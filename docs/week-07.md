# Week 7: Parametric CAD Design

**Goal this week:** Make 3D CAD models with perfect tolerances of the baffle. 

## What I did

- Transcribed my pen-and-paper sketches and mathematical calculations from Week 5 into highly specific text constraints, down to the exact millimeter offsets and 0.40 mm sliding clearances and fed into Gemini to generate precise structural prompts.
- Took those optimized prompts and fed them into an AI CAD agent (Zoo Design Studio / ZooKeeper AI) to generate the parametric code scripts (.kcl files).
- Generated four distinct components:
    1. main.kcl: The 94x94 mm, 8 mm thick base plate featuring custom 35x35 mm recessed pockets to      clamp the MG90 servos horizontally without glue, ensuring the splines align perfectly.
    2. middle.kcl: The free-floating central telescoping tube.
    3. topart.kcl: The top plate and baffle, featuring the dual 90 mm slotted rails (track for the      Scotch Yoke mechanism) aligned perfectly to the diagonal servo layout.
    4. arm.kcl: The custom 80 mm servo arms with a built-in 4 mm sliding pin to lock into the        slotted rails.
- Exported these models from Zoo Design Studio and imported them into Autodesk Fusion for final assembly verification. (Note: All finalized CAD files have been uploaded to the CAD section of the repo).

## Problems and blockers

- I simply didn't have the muscle memory in Fusion 360 to manually model complex interlocking sliding tubes and offset rails quickly enough for a sprint. Instead of fighting the software, I treated CAD generation like code generation. gave the AI agent perfectly structured, unambiguous prompts.


## Next week

- Move into fabrication and electronics. I need to 3D print these CAD files, assemble the stages, and write the Python code to run the servos via a Raspberry Pi.

