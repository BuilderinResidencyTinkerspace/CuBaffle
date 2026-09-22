#!/usr/bin/env python3
"""
CubeSat Baffle Controller — Phase 3 (3-tab GUI) + Smooth Motion
------------------------------------------------------------------
Tab 1: Control        — Stow / Deploy buttons + live log
Tab 2: Live Feed       — Pi Cam 3 MJPEG stream, auto-opens on deploy/stow,
                         "download last 15s" button (640x480 @24fps clip)
Tab 3: Analysis        — last-stowed vs last-deployed comparison: mean
                         brightness in a hardcoded glare ROI, diff heatmap,
                         one-line plain-English takeaway. Shows "no data
                         yet" until both states have been captured once.

Deploy/stow no longer snap instantly — the pulse width is ramped from the
current position to the target over MOVE_TIME_S using an eased
(smoothstep) curve, so the servos accelerate gently, cruise, and
decelerate gently. The comparison photo is captured right after the move
finishes settling, same as before.

PREREQUISITES:
    - pwm-2chan overlay already set up
    - Pi Cam 3 connected and enabled

INSTALL:
    sudo apt install python3-flask python3-opencv python3-picamera2

RUN:
    sudo python3 baffle_phase3.py

Then from a browser on the same WiFi:
    http://<pi-ip>:5000
"""

import atexit
import base64
import glob
import os
import sys
import threading
import time
from collections import deque
from datetime import datetime

import cv2
import numpy as np
from flask import Flask, Response, jsonify, render_template_string, request, send_file
from picamera2 import Picamera2

# ============================================================
# HARDCODED PWM VALUES — from your tuning session
# ============================================================
STOWED_US = 2300
DEPLOYED_US = 1600

# ---- Smooth motion settings ----
MOVE_TIME_S = 2.5    # how long a deploy/stow takes (bigger = slower/smoother)
STEP_S = 0.02         # update interval; matches the 20ms PWM period (50Hz)
SETTLE_S = 0.3        # extra wait after the ramp so the servos finish arriving
STARTUP_WAIT_S = 3    # wait after the startup snap (position is unknown then)
# ============================================================

FRAME_W, FRAME_H = 640, 480
STREAM_FPS = 24
CLIP_SECONDS = 15
RING_BUFFER_LEN = STREAM_FPS * CLIP_SECONDS

# Glare ROI in pixel coordinates (x1, y1, x2, y2) within a 640x480 frame.
# <<< REPLACE after you find where the stray light actually lands >>>
GLARE_ROI = (200, 150, 440, 330)

PERIOD_NS = 20_000_000
SYSFS_PWM_ROOT = "/sys/class/pwm"


def ease(t):
    """Smoothstep: 0 -> 1 with zero velocity at both ends (S-curve)."""
    return t * t * (3 - 2 * t)


# ---------------------------------------------------------------------
# Hardware PWM plumbing
# ---------------------------------------------------------------------
def find_pwmchip():
    candidates = sorted(glob.glob(f"{SYSFS_PWM_ROOT}/pwmchip*"))
    if not candidates:
        sys.exit("No pwmchip found. Check the pwm-2chan overlay and reboot.")
    for chip in candidates:
        try:
            with open(f"{chip}/npwm") as f:
                if int(f.read().strip()) >= 2:
                    return chip
        except (FileNotFoundError, ValueError):
            continue
    return candidates[0]


def write_sysfs(path, value):
    with open(path, "w") as f:
        f.write(str(value))


class HWPWM:
    def __init__(self, chip_path, channel, label):
        self.chip_path = chip_path
        self.channel = channel
        self.chan_path = f"{chip_path}/pwm{channel}"
        self.label = label
        self.current_us = None  # last commanded pulse; None = unknown yet
        self._export()
        write_sysfs(f"{self.chan_path}/period", PERIOD_NS)
        write_sysfs(f"{self.chan_path}/enable", 1)

    def _export(self):
        if not os.path.isdir(self.chan_path):
            write_sysfs(f"{self.chip_path}/export", self.channel)
            for _ in range(20):
                if os.path.isdir(self.chan_path):
                    break
                time.sleep(0.05)
            else:
                sys.exit(f"pwm{self.channel} did not appear after export.")

    def set_pulse(self, us):
        write_sysfs(f"{self.chan_path}/duty_cycle", int(us * 1000))
        self.current_us = us

    def close(self):
        try:
            write_sysfs(f"{self.chan_path}/enable", 0)
            write_sysfs(f"{self.chip_path}/unexport", self.channel)
        except OSError:
            pass


# ---------------------------------------------------------------------
# Shared state
# ---------------------------------------------------------------------
state_lock = threading.Lock()
state = "DEPLOYED"  # placeholder; forced STOWED at startup
busy = False
log_lines = []

frame_lock = threading.Lock()
latest_frame_jpeg = None
ring_buffer = deque(maxlen=RING_BUFFER_LEN)

comparison_lock = threading.Lock()
last_stowed_jpeg = None
last_deployed_jpeg = None
comparison_data = {"available": False}

servos = []
picam2 = None


def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    log_lines.append(f"[{ts}] {msg}")
    print(f"[{ts}] {msg}")


# ---------------------------------------------------------------------
# Smooth motion
# ---------------------------------------------------------------------
def move_smooth(target_us, duration_s):
    """Ramp every servo from its current pulse to target_us with easing."""
    starts = [sv.current_us for sv in servos]
    if any(s is None for s in starts):
        # Position unknown (nothing commanded yet) -> can't ramp, just snap.
        for sv in servos:
            sv.set_pulse(target_us)
        return

    t0 = time.monotonic()
    while True:
        frac = min((time.monotonic() - t0) / duration_s, 1.0)
        e = ease(frac)
        for sv, start in zip(servos, starts):
            sv.set_pulse(start + (target_us - start) * e)
        if frac >= 1.0:
            break
        time.sleep(STEP_S)


# ---------------------------------------------------------------------
# Camera background thread
# ---------------------------------------------------------------------
def camera_loop():
    global latest_frame_jpeg
    interval = 1.0 / STREAM_FPS
    while True:
        try:
            frame_rgb = picam2.capture_array()
            frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
            frame_bgr = cv2.resize(frame_bgr, (FRAME_W, FRAME_H))
            ok, jpeg = cv2.imencode(".jpg", frame_bgr, [cv2.IMWRITE_JPEG_QUALITY, 80])
            if ok:
                jpeg_bytes = jpeg.tobytes()
                with frame_lock:
                    latest_frame_jpeg = jpeg_bytes
                    ring_buffer.append(jpeg_bytes)
        except Exception as e:
            log(f"camera loop error: {e}")
        time.sleep(interval)


# ---------------------------------------------------------------------
# Comparison analysis (Tab 3)
# ---------------------------------------------------------------------
def decode_jpeg(jpeg_bytes):
    arr = np.frombuffer(jpeg_bytes, dtype=np.uint8)
    return cv2.imdecode(arr, cv2.IMREAD_COLOR)


def update_comparison():
    global comparison_data
    with comparison_lock:
        stow_bytes, dep_bytes = last_stowed_jpeg, last_deployed_jpeg

    if stow_bytes is None or dep_bytes is None:
        comparison_data = {"available": False}
        return

    stow_img = decode_jpeg(stow_bytes)
    dep_img = decode_jpeg(dep_bytes)
    x1, y1, x2, y2 = GLARE_ROI

    stow_roi_gray = cv2.cvtColor(stow_img[y1:y2, x1:x2], cv2.COLOR_BGR2GRAY)
    dep_roi_gray = cv2.cvtColor(dep_img[y1:y2, x1:x2], cv2.COLOR_BGR2GRAY)
    stow_mean = float(stow_roi_gray.mean())
    dep_mean = float(dep_roi_gray.mean())
    pct_change = ((stow_mean - dep_mean) / stow_mean * 100) if stow_mean > 0.01 else 0.0

    diff = cv2.absdiff(stow_img, dep_img)
    diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    diff_heat = cv2.applyColorMap(diff_gray, cv2.COLORMAP_JET)
    _, diff_jpeg = cv2.imencode(".jpg", diff_heat)

    direction = "dropped" if pct_change > 0 else "increased"
    sentence = (
        f"Stray light in the glare region {direction} by {abs(pct_change):.0f}% "
        f"when deployed compared to stowed."
    )

    comparison_data = {
        "available": True,
        "stow_mean": round(stow_mean, 1),
        "dep_mean": round(dep_mean, 1),
        "pct_change": round(pct_change, 1),
        "sentence": sentence,
        "stow_jpeg_b64": base64.b64encode(stow_bytes).decode(),
        "dep_jpeg_b64": base64.b64encode(dep_bytes).decode(),
        "diff_jpeg_b64": base64.b64encode(diff_jpeg.tobytes()).decode(),
        "roi": list(GLARE_ROI),
    }


def capture_state_photo(new_state):
    global last_stowed_jpeg, last_deployed_jpeg
    with frame_lock:
        frame_bytes = latest_frame_jpeg
    if frame_bytes is None:
        log("No camera frame available yet — skipping comparison capture.")
        return
    with comparison_lock:
        if new_state == "STOWED":
            last_stowed_jpeg = frame_bytes
        else:
            last_deployed_jpeg = frame_bytes
    update_comparison()


# ---------------------------------------------------------------------
# Servo move logic
# ---------------------------------------------------------------------
def drive_all(pulse_us, label, new_state, smooth=True):
    global busy, state
    busy = True
    try:
        if smooth:
            log(f"Moving to {label} ({pulse_us}us) over {MOVE_TIME_S}s...")
            move_smooth(pulse_us, MOVE_TIME_S)
            time.sleep(SETTLE_S)
        else:
            log(f"Moving to {label} ({pulse_us}us)... please wait {STARTUP_WAIT_S}s")
            for sv in servos:
                sv.set_pulse(pulse_us)
            time.sleep(STARTUP_WAIT_S)
        log(f"{label} complete.")
        with state_lock:
            state = new_state
        capture_state_photo(new_state)
    finally:
        busy = False


# ---------------------------------------------------------------------
# Flask app
# ---------------------------------------------------------------------
app = Flask(__name__)

PAGE = """
<!doctype html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Baffle Control</title>
<style>
  body { font-family: sans-serif; background: #111; color: #eee; text-align: center; padding: 10px; }
  h1 { font-size: 1.2em; }
  .tabs { display: flex; justify-content: center; margin-bottom: 10px; }
  .tab-btn {
    padding: 10px 18px; margin: 4px; border: none; border-radius: 6px;
    background: #333; color: #eee; cursor: pointer; font-size: 1em;
  }
  .tab-btn.active { background: #2d6cdf; }
  .tab-content { display: none; }
  .tab-content.active { display: block; }
  button.action {
    font-size: 1.1em; padding: 16px 28px; margin: 8px; border: none;
    border-radius: 8px; cursor: pointer; min-width: 120px;
  }
  #stow-btn { background: #2d6cdf; color: white; }
  #deploy-btn { background: #d94a3d; color: white; }
  button:disabled { opacity: 0.4; cursor: not-allowed; }
  #log {
    background: black; color: #0f0; text-align: left; padding: 10px;
    height: 220px; overflow-y: auto; border-radius: 6px; font-family: monospace;
    font-size: 0.8em; white-space: pre-wrap; margin-top: 10px;
  }
  img.feed { max-width: 100%; border-radius: 6px; }
  .cmp-imgs { display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; margin-top: 10px; }
  .cmp-imgs div { text-align: center; }
  .cmp-imgs img { width: 260px; border-radius: 6px; }
  #sentence { font-size: 1.15em; margin: 14px 0; padding: 10px; background: #222; border-radius: 6px; }
  #download-btn { padding: 10px 16px; margin-top: 10px; border-radius: 6px; border: none; background: #2d6cdf; color: white; cursor: pointer; }
</style>
</head>
<body>
  <h1>CubeSat Baffle Control</h1>
  <div class="tabs">
    <button class="tab-btn active" onclick="showTab(1)">Control</button>
    <button class="tab-btn" onclick="showTab(2)">Live Feed</button>
    <button class="tab-btn" onclick="showTab(3)">Analysis</button>
  </div>

  <div id="tab1" class="tab-content active">
    <div id="state">state: ...</div>
    <div>
      <button class="action" id="stow-btn" onclick="sendCmd('stow')">STOW</button>
      <button class="action" id="deploy-btn" onclick="sendCmd('deploy')">DEPLOY</button>
    </div>
    <div id="log"></div>
  </div>

  <div id="tab2" class="tab-content">
    <img class="feed" src="/video_feed">
    <div><button id="download-btn" onclick="downloadClip()">Download last 15s</button></div>
  </div>

  <div id="tab3" class="tab-content">
    <div id="cmp-placeholder">No data yet — deploy and stow at least once.</div>
    <div id="cmp-body" style="display:none;">
      <div id="sentence"></div>
      <div class="cmp-imgs">
        <div><div>Stowed</div><img id="stow-img"></div>
        <div><div>Deployed</div><img id="dep-img"></div>
        <div><div>Difference</div><img id="diff-img"></div>
      </div>
    </div>
  </div>

<script>
let lastCount = 0;

function showTab(n) {
  for (let i = 1; i <= 3; i++) {
    document.getElementById('tab' + i).classList.toggle('active', i === n);
  }
  const btns = document.querySelectorAll('.tab-btn');
  btns.forEach((b, i) => b.classList.toggle('active', i === n - 1));
}

async function sendCmd(cmd) {
  showTab(2);  // auto-switch to live feed on any move
  document.getElementById('stow-btn').disabled = true;
  document.getElementById('deploy-btn').disabled = true;
  await fetch('/' + cmd, { method: 'POST' });
}

function downloadClip() {
  window.location = '/download_clip';
}

async function pollStatus() {
  const res = await fetch('/status?since=' + lastCount);
  const data = await res.json();
  document.getElementById('state').innerText = 'state: ' + data.state +
      (data.busy ? '  (moving...)' : '');
  const logDiv = document.getElementById('log');
  for (const line of data.new_logs) {
    logDiv.innerText += line + '\\n';
  }
  logDiv.scrollTop = logDiv.scrollHeight;
  lastCount = data.count;
  document.getElementById('stow-btn').disabled = data.busy;
  document.getElementById('deploy-btn').disabled = data.busy;
}

async function pollComparison() {
  const res = await fetch('/comparison_data');
  const data = await res.json();
  if (!data.available) {
    document.getElementById('cmp-placeholder').style.display = 'block';
    document.getElementById('cmp-body').style.display = 'none';
    return;
  }
  document.getElementById('cmp-placeholder').style.display = 'none';
  document.getElementById('cmp-body').style.display = 'block';
  document.getElementById('sentence').innerText = data.sentence +
      '  (stowed=' + data.stow_mean + ', deployed=' + data.dep_mean + ')';
  document.getElementById('stow-img').src = 'data:image/jpeg;base64,' + data.stow_jpeg_b64;
  document.getElementById('dep-img').src = 'data:image/jpeg;base64,' + data.dep_jpeg_b64;
  document.getElementById('diff-img').src = 'data:image/jpeg;base64,' + data.diff_jpeg_b64;
}

setInterval(pollStatus, 600);
setInterval(pollComparison, 2000);
pollStatus();
pollComparison();
</script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(PAGE)


@app.route("/status")
def status():
    since = int(request.args.get("since", 0))
    with state_lock:
        new_logs = log_lines[since:]
        return jsonify(state=state, busy=busy, new_logs=new_logs, count=len(log_lines))


@app.route("/deploy", methods=["POST"])
def deploy():
    with state_lock:
        if busy:
            log("Command ignored — a move is already in progress.")
            return jsonify(ok=False), 409
        if state == "DEPLOYED":
            log("already deployed")
            return jsonify(ok=True)
    drive_all(DEPLOYED_US, "DEPLOYED", "DEPLOYED")
    return jsonify(ok=True)


@app.route("/stow", methods=["POST"])
def stow():
    with state_lock:
        if busy:
            log("Command ignored — a move is already in progress.")
            return jsonify(ok=False), 409
        if state == "STOWED":
            log("already stowed")
            return jsonify(ok=True)
    drive_all(STOWED_US, "STOWED", "STOWED")
    return jsonify(ok=True)


def gen_mjpeg():
    interval = 1.0 / STREAM_FPS
    while True:
        with frame_lock:
            frame = latest_frame_jpeg
        if frame is not None:
            yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
        time.sleep(interval)


@app.route("/video_feed")
def video_feed():
    return Response(gen_mjpeg(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/download_clip")
def download_clip():
    with frame_lock:
        frames_copy = list(ring_buffer)
    if not frames_copy:
        return "No frames captured yet", 404

    tmp_path = f"/tmp/baffle_clip_{int(time.time())}.mp4"
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(tmp_path, fourcc, STREAM_FPS, (FRAME_W, FRAME_H))
    for jpeg_bytes in frames_copy:
        img = decode_jpeg(jpeg_bytes)
        if img is not None:
            writer.write(img)
    writer.release()

    return send_file(tmp_path, as_attachment=True, download_name="last_15s.mp4")


@app.route("/comparison_data")
def comparison_data_endpoint():
    return jsonify(comparison_data)


def cleanup():
    log("Shutting down: driving to STOWED before exit...")
    with state_lock:
        cur_state = state
    if cur_state != "STOWED":
        drive_all(STOWED_US, "STOWED (shutdown)", "STOWED")
    else:
        log("Already stowed — no move needed before shutdown.")
    for sv in servos:
        sv.close()
    if picam2 is not None:
        picam2.stop()
    log("Shut down cleanly.")


def main():
    global servos, state, picam2

    if os.geteuid() != 0:
        sys.exit("This needs root to write to /sys/class/pwm. Run with: sudo python3 baffle_phase3.py")

    chip = find_pwmchip()
    log(f"Using {chip}")
    servos = [HWPWM(chip, 0, "servo A"), HWPWM(chip, 1, "servo B")]

    log("Starting camera...")
    picam2 = Picamera2()
    config = picam2.create_video_configuration(main={"size": (FRAME_W, FRAME_H), "format": "RGB888"})
    picam2.configure(config)
    picam2.start()
    time.sleep(1)  # let auto-exposure settle
    threading.Thread(target=camera_loop, daemon=True).start()

    # Startup: actively drive to STOWED, don't just assume it.
    # Position is unknown at this point, so this one move is a direct snap.
    drive_all(STOWED_US, "STOWED (startup)", "STOWED", smooth=False)

    atexit.register(cleanup)

    try:
        app.run(host="0.0.0.0", port=5000, threaded=True)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
