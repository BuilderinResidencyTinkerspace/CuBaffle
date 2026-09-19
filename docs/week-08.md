# Week 8: Fabrication, Assembly, and Electronics

**Goal this week:** The main objective is to 3D print the entire three-stage baffle and get the mechanical setup done and also to get the required electronics working.  

## What I did

- I 3D printed the entire baffle assembly, which consists of the top plate (with the upper segment), the middle segment, and the bottom plate (with the lower segment).
- Right away, I ran into a major assembly issue based on how the tolerances were built. The original design had the lower baffle segment fused directly to the bottom base plate. Because of the overlapping lips on the tubes, it was physically impossible to slide the middle segment over it during assembly.
- To fix this issue I went back and printed the lower baffle segment as a completely separate piece. Once I slid the middle segment over it and had the tubes correctly nested, I just super-glued the lower segment down to the bottom plate. The assembled baffle perfectly fits together now, and you can see the fully nested structure and top plate in the photos.
  <img width="768" height="1024" alt="image" src="https://github.com/user-attachments/assets/2b18a011-81c1-4b72-b65a-a64f09effdf0" />
<img width="768" height="1024" alt="image" src="https://github.com/user-attachments/assets/daf272ca-30ca-4fd6-92eb-5de9c566553f" />
<img width="768" height="1024" alt="image" src="https://github.com/user-attachments/assets/86e4c5b2-5dd7-481d-8665-66b2cca969d5" />

- **Note:** Ideally, an optical baffle should be printed in matte black to absorb maximum stray light. Unfortunately, I only had a white spool lying around, so I printed it in white for now to verify the mechanics. I will upgrade to black filament in the coming weeks if possible.
  
- On the electrical side, I locked in the final component list. I originally thought about using a 3-cell LiPo to power everything, but dropped that idea. Instead, I went with a simple 4x AA battery pack (giving the required 6V) dedicated just to the two MG90s servo motors. The Raspberry Pi 5 is powered completely separately by its official power supply.
- Wired everything up on a perf board. The ground from the battery pack is tied to Pi pin 39 to create a common ground with the servos. Since both servos mirror the exact same movement, they both receive their PWM signal from a single pin (Pi pin 32). Currently, there isn't a power switch for the servos; they just turn on as soon as the batteries are slotted in.
- I set up the electrical connections on a separate test bench and wrote the Python control software. The code features a clean state machine (toggling between STOWED and DEPLOYED) and uses hardware PWM so the servos don't jitter. It runs a simple command-line interface where I can type commands to move the servos using placeholder PWM values. I also added a safety feature in the code that automatically forces the servos back to the stowed position before the script shuts down.
- Right now, the mechanical baffle works, and the electronics/code work perfectly on the bench, but they haven't been physically integrated together yet.


## Next week

- Full system integration. I need to physically mount the servos into the base plate, attach the arms to the top plate, and get the code to successfully lift the actual printed baffle.

## Links

- Code:
- Photos / CAD:
