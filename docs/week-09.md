# Week 9: Full System Integration & Web Dashboard

**Goal this week:**: Physically integrate the mechanical baffle with the electronics, finalize the software control system with a proper user interface, and pack everything into the 1U CubeSat chassis.

## What I did

- Mounted the servos to the bottom plate of the baffle and attempted to slot the 80mm arms into the tracking rails on the top plate. Unfortunately the arms jammed mid-stroke inside the rails, locking the entire mechanism and stalling out both servos.
- I spent time iterating the servo arms, shortening them from 8cm down to 7.5cm and making minor dimensional tweaks, but the binding persisted. It became clear that the slotted rails themselves needed a total redesign.
- Doing a proper redesign of the rails meant 3D printing a brand new top plate, and I just didn't have the time left in the sprint for that. So, went with a functional workaround to bypass the rails. Now the servo arms just push directly against the flat underside of the top plate.
- It actually deploys and stows incredibly smoothly now. With the tradeoff that without the rails keeping it constrained, the baffle twists a little bit as it rises and sometimes sits at a slight angle when fully deployed.
- Software Dashboard: Completely upgraded the Python controller. I built a web-based dashboard using flask that can be accessed over Wi-Fi by any device. It features three main tabs:
  1. Control Tab: Simple buttons to Deploy and Stow, alongside a live system log.
  2. Live Feed Tab: Streams real-time MJPEG video from the Pi Cam 3, complete with a button to download the last 15 seconds of footage.
  3. Analysis Tab: Automatically captures a frame when the baffle is stowed and another when deployed. It calculates the mean brightness in a predefined "glare" region, outputs a plain-English verdict on whether stray light increased or dropped, and generates a visual heatmap showing exactly where the light differences occurred.
- Rewrote the servo driving logic to use a "smoothstep" mathematical S-curve. Instead of snapping violently from one position to the next, the servos now gently accelerate, cruise, and smoothly decelerate over a 2.5-second window.
- **Final Assembly:** I placed the entire functioning stack the Raspberry Pi 5, the Pi Cam (mounted underneath looking up through the baffle), the servos, and the 3D-printed baffle inside the clear laser-cut 1U acrylic chassis. Only the 6V AA battery pack and the Pi's power brick sit outside the box.


