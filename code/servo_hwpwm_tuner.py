#!/usr/bin/env python3
"""
MG90S Manual PWM Tuner — Raspberry Pi 5, TRUE HARDWARE PWM
------------------------------------------------------------
Same idea as the earlier tuner, but drives the servos through the RP1's
dedicated PWM hardware blocks via the Linux sysfs pwm interface, instead
of gpiozero's software-timed PWM. This removes the CPU-load jitter you
saw with the lgpio-backed version.

PREREQUISITE — you must have already added this to /boot/firmware/config.txt
and rebooted:
    dtoverlay=pwm-2chan,pin=12,func=4,pin2=13,func2=4

That puts GPIO12 on hardware PWM channel 0, and GPIO13 on channel 1,
both under the same pwmchip (usually pwmchip0 or pwmchip2 depending on
firmware version — the script auto-detects it).

WIRING:
    Servo 1 signal -> GPIO12 (physical pin 32)  -> pwm channel 0
    Servo 2 signal -> GPIO13 (physical pin 33)  -> pwm channel 1
    Servo V+       -> external 5-6V supply, NOT the Pi's 5V rail
    Servo GND      -> common ground with the Pi AND the external supply

PERMISSIONS: writing to /sys/class/pwm requires root (or a udev rule).
Simplest for now:
    sudo python3 servo_hwpwm_tuner.py

RUN (live jog UI, default):
    sudo python3 servo_hwpwm_tuner.py

RUN (plain text input):
    sudo python3 servo_hwpwm_tuner.py --manual

Live-jog controls:
    1 / 2       select servo 1 or 2
    Up / Down   +/- coarse step (default 50us)
    Left/Right  +/- fine step (default 5us)
    [ / ]       decrease / increase the coarse step size
    c           center both (1500us)
    d           disable PWM on selected servo (no holding torque)
    r           re-enable PWM on selected servo
    s           print current values on screen as a snippet
    q           quit (prints final values, cleans up sysfs exports)
"""

import argparse
import curses
import glob
import os
import sys
import time

PERIOD_NS = 20_000_000  # 20ms = 50Hz, fixed for standard hobby servos
SYSFS_PWM_ROOT = "/sys/class/pwm"


def find_pwmchip():
    """Find the pwmchip exposing at least 2 channels (from pwm-2chan overlay)."""
    candidates = sorted(glob.glob(f"{SYSFS_PWM_ROOT}/pwmchip*"))
    if not candidates:
        sys.exit(
            "No pwmchip found under /sys/class/pwm.\n"
            "Did you add 'dtoverlay=pwm-2chan,pin=12,func=4,pin2=13,func2=4'\n"
            "to /boot/firmware/config.txt and reboot?"
        )
    for chip in candidates:
        try:
            with open(f"{chip}/npwm") as f:
                npwm = int(f.read().strip())
            if npwm >= 2:
                return chip
        except (FileNotFoundError, ValueError):
            continue
    # fall back to the first chip found even if npwm looked odd
    return candidates[0]


def write_sysfs(path, value):
    with open(path, "w") as f:
        f.write(str(value))


def read_sysfs(path):
    with open(path) as f:
        return f.read().strip()


class HWPWM:
    """Thin wrapper around one /sys/class/pwm/<chip>/pwm<N> channel."""

    def __init__(self, chip_path, channel, label, min_us, max_us, start_us):
        self.chip_path = chip_path
        self.channel = channel
        self.chan_path = f"{chip_path}/pwm{channel}"
        self.label = label
        self.min_us = min_us
        self.max_us = max_us
        self.pulse_us = start_us
        self.enabled = True

        self._export()
        write_sysfs(f"{self.chan_path}/period", PERIOD_NS)
        self.apply()
        write_sysfs(f"{self.chan_path}/enable", 1)

    def _export(self):
        if not os.path.isdir(self.chan_path):
            try:
                write_sysfs(f"{self.chip_path}/export", self.channel)
            except OSError as e:
                sys.exit(f"Failed exporting pwm channel {self.channel}: {e}")
            for _ in range(20):
                if os.path.isdir(self.chan_path):
                    break
                time.sleep(0.05)
            else:
                sys.exit(f"pwm{self.channel} did not appear after export.")

    def clamp(self, us):
        return max(self.min_us, min(self.max_us, us))

    def set_pulse(self, us):
        self.pulse_us = self.clamp(us)
        if self.enabled:
            self.apply()

    def apply(self):
        duty_ns = int(self.pulse_us * 1000)
        write_sysfs(f"{self.chan_path}/duty_cycle", duty_ns)

    def disable(self):
        self.enabled = False
        write_sysfs(f"{self.chan_path}/enable", 0)

    def enable(self):
        self.enabled = True
        write_sysfs(f"{self.chan_path}/enable", 1)
        self.apply()

    def close(self):
        try:
            write_sysfs(f"{self.chan_path}/enable", 0)
            write_sysfs(f"{self.chip_path}/unexport", self.channel)
        except OSError:
            pass


def run_curses(servos, coarse_step, fine_step):
    def main(stdscr):
        curses.curs_set(0)
        selected = 0
        step = coarse_step
        message = ""

        def draw():
            stdscr.clear()
            stdscr.addstr(0, 0, "MG90S Manual PWM Tuner (hardware PWM)  (q to quit)")
            stdscr.addstr(1, 0, "-" * 60)
            for i, sv in enumerate(servos):
                marker = ">" if i == selected else " "
                state = "ON " if sv.enabled else "OFF"
                stdscr.addstr(
                    3 + i, 0,
                    f"{marker} Servo {i+1} [{sv.label}] pwm{sv.channel}: "
                    f"{sv.pulse_us:7.1f} us  ({state})  "
                    f"range [{sv.min_us:.0f}-{sv.max_us:.0f}]"
                )
            row = 3 + len(servos)
            stdscr.addstr(row + 1, 0, f"Step size: {step:.0f} us   ( [ / ] to change )")
            stdscr.addstr(row + 3, 0,
                          "1/2 select | Up/Down +/- step | Left/Right +/- 5us fine")
            stdscr.addstr(row + 4, 0,
                          "c center-both | d disable | r enable | s snippet | q quit")
            if message:
                stdscr.addstr(row + 6, 0, message)
            stdscr.refresh()

        draw()
        while True:
            key = stdscr.getch()
            sv = servos[selected]
            message = ""
            if key in (ord('1'), ord('2')):
                idx = key - ord('1')
                if idx < len(servos):
                    selected = idx
            elif key == curses.KEY_UP:
                sv.set_pulse(sv.pulse_us + step)
            elif key == curses.KEY_DOWN:
                sv.set_pulse(sv.pulse_us - step)
            elif key == curses.KEY_RIGHT:
                sv.set_pulse(sv.pulse_us + fine_step)
            elif key == curses.KEY_LEFT:
                sv.set_pulse(sv.pulse_us - fine_step)
            elif key == ord('['):
                step = max(1, step - 5)
            elif key == ord(']'):
                step += 5
            elif key == ord('c'):
                for s in servos:
                    s.set_pulse(1500)
            elif key == ord('d'):
                sv.disable()
            elif key == ord('r'):
                sv.enable()
            elif key == ord('s'):
                message = "CURRENT: " + "  ".join(
                    f"S{i+1}={s.pulse_us:.0f}us" for i, s in enumerate(servos)
                )
            elif key == ord('q'):
                break
            draw()

    curses.wrapper(main)


def run_manual(servos):
    print("Manual mode. Commands:")
    print("  s1 <us>   set servo 1 pulse width, e.g.  s1 1230")
    print("  s2 <us>   set servo 2 pulse width")
    print("  center    set both to 1500us")
    print("  show      print current values")
    print("  d1 / d2   disable servo 1/2 (no holding torque)")
    print("  r1 / r2   re-enable servo 1/2")
    print("  q         quit")
    while True:
        try:
            cmd = input("> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            break
        if cmd in ("q", "quit", "exit"):
            break
        elif cmd == "center":
            for sv in servos:
                sv.set_pulse(1500)
        elif cmd == "show":
            for i, sv in enumerate(servos):
                print(f"  Servo {i+1}: {sv.pulse_us:.1f} us (enabled={sv.enabled})")
        elif cmd in ("d1", "d2"):
            servos[int(cmd[1]) - 1].disable()
        elif cmd in ("r1", "r2"):
            servos[int(cmd[1]) - 1].enable()
        elif cmd.startswith("s1 ") or cmd.startswith("s2 "):
            idx = int(cmd[1]) - 1
            try:
                us = float(cmd.split()[1])
            except (IndexError, ValueError):
                print("  usage: s1 1500")
                continue
            servos[idx].set_pulse(us)
            print(f"  Servo {idx+1} -> {servos[idx].pulse_us:.1f} us")
        else:
            print("  unknown command")


def main():
    if os.geteuid() != 0:
        sys.exit("This needs root to write to /sys/class/pwm. Run with: sudo python3 servo_hwpwm_tuner.py")

    parser = argparse.ArgumentParser(
        description="Manual HARDWARE PWM tuner for 2x MG90S servos on Raspberry Pi 5"
    )
    parser.add_argument("--chan1", type=int, default=0, help="pwm channel for servo 1 (default 0 = GPIO12)")
    parser.add_argument("--chan2", type=int, default=1, help="pwm channel for servo 2 (default 1 = GPIO13)")
    parser.add_argument("--min-us", type=float, default=500, help="minimum allowed pulse width (default 500)")
    parser.add_argument("--max-us", type=float, default=2500, help="maximum allowed pulse width (default 2500)")
    parser.add_argument("--start-us", type=float, default=1500, help="starting pulse width (default 1500)")
    parser.add_argument("--coarse-step", type=float, default=50, help="live-jog coarse step in us (default 50)")
    parser.add_argument("--fine-step", type=float, default=5, help="live-jog fine step in us (default 5)")
    parser.add_argument("--manual", action="store_true", help="plain text input instead of the live-jog UI")
    args = parser.parse_args()

    chip = find_pwmchip()
    print(f"Using {chip}")

    servos = [
        HWPWM(chip, args.chan1, "servo A", args.min_us, args.max_us, args.start_us),
        HWPWM(chip, args.chan2, "servo B", args.min_us, args.max_us, args.start_us),
    ]

    try:
        if args.manual:
            run_manual(servos)
        else:
            run_curses(servos, args.coarse_step, args.fine_step)
    finally:
        print("\nFinal pulse widths (write these down):")
        for i, sv in enumerate(servos):
            print(f"  Servo {i+1} (pwm{sv.channel}): {sv.pulse_us:.1f} us")
        for sv in servos:
            sv.close()


if __name__ == "__main__":
    main()
