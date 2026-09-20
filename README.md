# Cubaffle - Deployable Optical Baffle Demonstrator 
This repository contains the complete documentation, CAD files, and control software to build a ground-based functional prototype of a deployable optical baffle for a 1U CubeSat. The project aims to solve the volume vs. accuracy contradiction in high-accuracy star trackers by utilizing a 3-stage telescoping baffle that stows completely within a 1U chassis (10x10x10 cm) and deploys to 8 cm using a dual-servo Scotch Yoke mechanism.

## Repository Structure

- `docs/` — roject overview, mathematical kinematic models, and weekly sprint logs documenting the engineering process, trade studies, and troubleshooting.
- `code/` — Python firmware and scripts to run the hardware PWM, command-line interface, and the web-based visual analysis dashboard.
- `cad/` — 3D models (.step, .kcl, .stl) for the 3-stage telescoping baffle and servo mechanisms, plus the 2D vector file (.svg) for the laser-cut acrylic CubeSat chassis.

## Hardware Bill of Materials (BOM)

- Compute & Optics: Raspberry Pi 5, Raspberry Pi Camera Module 3.
- Actuation: 2x MG90S Micro Servos.
- Power: 4x AA Battery Holder (supplying a dedicated 6V to servos), standard RPi 5 power supply.
- Chassis: 2.88mm transparent acrylic sheet (for laser cutting).
- Baffle: 3D Printer filament (Matte Black recommended for optical testing; PLA/PETG acceptable).
- Misc: Perf board, jumper wires, M2.5/M3 screws, super glue, liquid dish soap (for plastic lubrication).

## Fabrication & Assembly
1. Laser Cut the Chassis: Use the provided .svg file in the cad/ directory to laser cut the 1U CubeSat body out of 2.88mm acrylic. The standard CubeSat rails have been omitted to simplify ground testing.
2. 3D Print the Baffle: Print the base plate, middle segment, and top plate.
   - Crucial Assembly Note: Due to the overlapping retaining lips (0.40mm clearance), the lower baffle segment cannot be printed directly onto the base plate if you want to assemble the middle stage over it. Print the lower baffle segment as a separate piece, slide the middle segment over it, and then super-glue the lower segment to the base plate.
3. Mechanism Setup: Mount the MG90S servos into the base plate pockets. Attach the custom 7.5cm / 8.0cm servo arms.
4. Lubrication: Sand the layer lines of the 3D-printed cylinders smooth and apply a single drop of liquid dish soap to the sliding surfaces to prevent binding. Do not use Vaseline.

## Electronics & Wiring
To prevent torque spikes from browning out or damaging the Raspberry Pi, the servos must be powered by a completely isolated 6V power supply (the 4x AA pack) with a shared common ground.
Component,Wire / Pin,Connection Destination
Raspberry Pi 5,Pin 32 (GPIO 12 / PWM0),Splices to the Signal (Yellow/Orange) wires on both MG90s servos.
Raspberry Pi 5,Pin 39 (Ground),Connects to the Negative (Black) wire of the battery pack.
6V Battery Pack,Positive (Red),Splices to the VCC (Red) wires on both servos.
6V Battery Pack,Negative (Black),Connects to Pi Pin 39 and Ground (Brown/Black) on both servos.
Pi Cam 3,MIPI Ribbon Cable,Connects directly to the RPi 5 camera port.


First-time setup:

1. Push once and let the Action finish. It creates a `gh-pages` branch.
2. Settings → Pages → Source: **Deploy from a branch** → `gh-pages` / `root`.

Your site will be live at `https://<org-or-user>.github.io/<repo>/`.


## Weekly logs

Fill in `docs/week-01.md` through `docs/week-09.md` as you go. Keep them short: what you did, what's blocking you, what's next.
