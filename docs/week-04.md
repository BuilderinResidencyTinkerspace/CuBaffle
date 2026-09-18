# Week 4: CAD Basics & 1U Enclosure Fabrication

**Goal this week:** Get hands-on with CAD software and actually build the physical 1U CubeSat chassis that will house the deployable baffle prototype.

## What I did

- Installed and spent time exploring Fusion 360 for 3D modeling and Inkscape for 2D vector graphics.
- Looked into the mechanical concept of press-fits and sliding clearances, which will be crucial for making the telescoping tubes of the baffle work later on.
- Designed the 1U CubeSat body based on standard 10 cm x 10 cm x 10 cm outer dimensions. I used an open-source box generator (boxes.hackerspace-bamberg.de) to create the initial design using finger joints.
- Modified the SVG file in Inkscape to be laser-cut from 2.88mm thick transparent acrylic. Taking the roughly 2.8mm wall thickness into account, I calculated the exact usable inner space to be 94.4 mm x 94.4 mm. This is the hard physical boundary my stowed baffle has to fit inside. (Note: This SVG file is in the CAD file's section)
- Successfully laser cut and assembled the transparent acrylic box.
  <img width="1029" height="1280" alt="image" src="https://github.com/user-attachments/assets/fa64e68c-9858-4717-aa88-784f81df6f1b" />


## Problems and blockers

- According to the official CubeSat Design Specification, standard 1U CubeSats require specific rails (minimum 8.5mm width) along their edges so they can slide smoothly out of a standard P-POD deployer.
- Trying to integrate these rails into a flat laser-cut acrylic design adds a lot of unnecessary structural complexity.
  <img width="1346" height="821" alt="image" src="https://github.com/user-attachments/assets/d25befd6-b4c8-4af7-9b83-02d46c54a846" />


## Decisions

- I decided to completely remove the standard CubeSat rails from my design, since this is a ground-based prototype. Dropping them kept the fabrication fast and simple.

## Next week

- Make designs of baffle and servo mechanism.  

## Links
- Box design generator: https://boxes.hackerspace-bamberg.de/?language=en
- CubeSat Design Specification (CDS Rev 14): https://static1.squarespace.com/static/5418c831e4b0fa4ecac1bacd/t/62193b7fc9e72e0053f00910/1645820809779/CDS+REV14_1+2022-02-09.pdf

