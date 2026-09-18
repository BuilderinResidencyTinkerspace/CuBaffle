# Week 5: Mechanism Sketches & Mathematical Modeling

**Goal this week:** Figure out the exact math for the baffle stages, lock in the physical dimensions, sketch the mechanism, and prove the MG90 servos can actually lift it without jamming.

## What we did

- Sat down and made proper pen-and-paper sketches of the baffle and its lifting mechanisms, putting real dimensions to the ideas. Sketched out the top, side, and bottom views of the stowed and deployed states.
- Finalized the structural plan: it will be a 3-stage deployable baffle with a stowed length of 35mm and a fully deployed length of 80mm.
- Calculated the exact inner and outer radii for each stage. Assuming a 2mm wall thickness and a 0.4mm sliding clearance gap for 3D printing, the dimensions are: Innermost stage (7.78mm inner / 9.78mm outer), Middle stage (10.18mm inner / 12.18mm outer), and Outermost stage (12.58mm inner / 14.58mm outer).
- Compiled all these computations, along with the mechanical constraints, into a detailed document titled Baffle_Kinematics_and_Torque_Analysis.md (Note: this is uploaded in the repo documentation section).
  <img width="768" height="1024" alt="image" src="https://github.com/user-attachments/assets/f12fbdf4-88fa-4395-bc0f-06098ac76ec2" />
  <img width="768" height="1024" alt="image" src="https://github.com/user-attachments/assets/c0e405b8-3007-4c70-9e7b-cf901722b646" />
<img width="768" height="1024" alt="image" src="https://github.com/user-attachments/assets/18a46867-fbfa-44df-9cde-d0d62f694495" />




## Problems and blockers

- I was worried if two tiny MG90s servos could handle lifting the entire 3-stage baffle assembly, especially since the lever arm needs to be 8cm long to achieve the 4.5cm vertical stroke.
- Because the servos sit on opposite sides, pushing up could introduce a twisting rotational torque. With only a tight 0.40mm clearance between the walls, any slight twist causes the 3D-printed layer lines to catch, triggering a mechanical jam

## Decisions

- Ran a proper torque study (included in the Baffle_Kinematics_and_Torque_Analysis.md doc) and confirmed the MG90s definitely have the strength to lift the required weight at that arm length.
- To prevent the tubes from locking up, I decided that every segment will be sanded incredibly smooth during fabrication. I also decided to use liquid dish soap as a quick DIY lubricant between the stages to reduce friction. 

## Next week

- Start building out the parametric CAD models of the baffle. (Though looking at the calendar, Onam is coming up, so the schedule might shift)


