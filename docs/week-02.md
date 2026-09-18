# Week 2: Literature Review & Optical Baffle Fundamentals

**Goal this week:** Dive deep into academic literature and technical papers to understand how optical baffles are actually designed, how deployable mechanisms work in CubeSats, and what fabrication methods are feasible for prototyping.

## What I did

- Studied the core optical theory behind traditional fixed baffles, specifically the geometric rules laid out by Arnoux (1996) and Heinisch & Jolliffe (1971).
- Reviewed the traditional graphical design method versus analytical models for vane positioning. While classical designs rely on manual CAD ray-tracing to place vanes at the intersection of the field of view (FoV) boundary, modern approaches use parametric analytical equations to compute vane coordinates.
- Examined how existing space missions handle deployable structures, noting that CubeSats traditionally use deployables for solar panels and antennas, but rarely for optics due to tight alignment tolerances.
- Read through key papers on deployable baffles to see how different groups tackle the mechanism

## Problems and blockers

- The math behind conical deployable baffles gets tricky fast because of the wall thickness and overlapping stop-tab clearances between nested stages.

## Decisions

- I threw out the traditional "optics-first" mathematical approach.
- Instead, I decided to reverse-engineer the system based on fabrication requirements. I will design the mechanical structure first, basing the segment lengths, wall thicknesses, and sliding clearances on what I can reliably 3D print and only then apply the necessary optical features to fit within those physical constraints.

## Next week
- Do a full trade study on various deployment mechanisms to lock in exactly how the baffle will deploy and stove itself.

## References
Yalagach et al. (2024) - Development of a deployable mechanism for a conical optical baffle for a small satellite
Liu et al. (2021) - A compressed and high-accuracy star tracker with on-orbit deployable baffle for remote sensing cubesats
Arnoux (1996) - Star sensor baffle optimization: some helpful practical design rules

