#!/usr/bin/env python3
"""
CubeSat Baffle Deploy/Stow Controller — Iteration 1
------------------------------------------------------
State machine with two states: STOWED and DEPLOYED.
Both servos always move together to the same hardcoded pulse width
for a given state. Uses hardware PWM (RP1 pwm0/pwm1) for jitter-free
timing — same base as servo_hwpwm_tuner.py.

PREREQUISITE (already done):
    /boot/firmware/config.txt contains:
        dtoverlay=pwm-2chan,pin=12,func=4,pin2=13,func2=4
    and the Pi has been rebooted since.

>>> REPLACE THESE TWO VALUES with what you found using the tuner <<<
"""

import glob
import os
import sys
import time

PERIOD_NS = 20_000_000  # 20ms period = 50Hz, standard for hobby servos
SYSFS_PWM_ROOT = "/sys/class/pwm"

# ============================================================
# HARDCODED PWM VALUES — set these from your tuning session
# ============================================================
STOWED_US = 1500      # <- pulse width (us) that holds the baffle stowed
DEPLOYED_US = 2000    # <- pulse width (us) that holds the baffle deployed
MOVE_WAIT_S = 3        # seconds to block while the servos physically travel
# ============================================================


def find_pwmchip():
    """Find the pwmchip exposing at least 2 channels (from the pwm-2chan overlay)."""
    candidates = sorted(glob.glob(f"{SYSFS_PWM_ROOT}/pwmchip*"))
    if not candidates:
        sys.exit(
            "No pwmchip found under /sys/class/pwm.\n"
            "Check that the pwm-2chan overlay is in /boot/firmware/config.txt\n"
            "and that you've rebooted since adding it."
        )
    for chip in candidates:
        try:
            with open(f"{chip}/npwm") as f:
                npwm = int(f.read().strip())
            if npwm >= 2:
                return chip
        except (FileNotFoundError, ValueError):
            continue
    return candidates[0]


def write_sysfs(path, value):
    with open(path, "w") as f:
        f.write(str(value))


class HWPWM:
    """One /sys/class/pwm/<chip>/pwm<N> hardware PWM channel, fixed 50Hz."""

    def __init__(self, chip_path, channel, label):
        self.chip_path = chip_path
        self.channel = channel
        self.chan_path = f"{chip_path}/pwm{channel}"
        self.label = label
        self.pulse_us = None

        self._export()
        write_sysfs(f"{self.chan_path}/period", PERIOD_NS)
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

    def set_pulse(self, us):
        self.pulse_us = us
        write_sysfs(f"{self.chan_path}/duty_cycle", int(us * 1000))

    def close(self):
        try:
            write_sysfs(f"{self.chan_path}/enable", 0)
            write_sysfs(f"{self.chip_path}/unexport", self.channel)
        except OSError:
            pass


def drive_all(servos, pulse_us, label):
    print(f"Moving to {label} ({pulse_us}us)... please wait {MOVE_WAIT_S}s")
    for sv in servos:
        sv.set_pulse(pulse_us)
    time.sleep(MOVE_WAIT_S)
    print(f"{label} complete.")


def main():
    if os.geteuid() != 0:
        sys.exit("This needs root to write to /sys/class/pwm. Run with: sudo python3 baffle_control.py")

    chip = find_pwmchip()
    print(f"Using {chip}")

    servos = [
        HWPWM(chip, 0, "servo A"),
        HWPWM(chip, 1, "servo B"),
    ]

    state = "DEPLOYED"  # force the first drive_all below to actually move to STOWED
    try:
        # Startup: actively drive to STOWED, don't just assume it.
        drive_all(servos, STOWED_US, "STOWED (startup)")
        state = "STOWED"

        print("\nCommands: deploy | stow | status | quit\n")
        while True:
            cmd = input(f"[{state}] > ").strip().lower()

            if cmd in ("q", "quit", "exit"):
                break

            elif cmd == "deploy":
                if state == "DEPLOYED":
                    print("already deployed")
                else:
                    drive_all(servos, DEPLOYED_US, "DEPLOYED")
                    state = "DEPLOYED"

            elif cmd == "stow":
                if state == "STOWED":
                    print("already stowed")
                else:
                    drive_all(servos, STOWED_US, "STOWED")
                    state = "STOWED"

            elif cmd == "status":
                print(f"current state: {state}")

            else:
                print("commands: deploy | stow | status | quit")

    except KeyboardInterrupt:
        print("\n(Ctrl+C caught)")

    finally:
        # Shutdown: always leave the baffle stowed before closing.
        if state != "STOWED":
            drive_all(servos, STOWED_US, "STOWED (shutdown)")
        else:
            print("Already stowed — no move needed before shutdown.")
        for sv in servos:
            sv.close()
        print("Shut down cleanly.")


if __name__ == "__main__":
    main()
