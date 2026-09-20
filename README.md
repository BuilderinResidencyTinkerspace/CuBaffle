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

## Software Setup
The control software utilizes the Raspberry Pi's hardware PWM blocks to ensure jitter-free servo motion.
Step 1: Enable Hardware PWM
Open your /boot/firmware/config.txt and append the following line to enable the 2-channel PWM overlay:   
`dtoverlay=pwm-2chan,pin=12,func=4,pin2=13,func2=4`
Reboot the Raspberry Pi after saving.

Step 2: Install Dependencies
Install the required Python packages for the web dashboard and camera stream:
First-time setup:

`sudo apt update
sudo apt install python3-flask python3-opencv python3-picamera2`


