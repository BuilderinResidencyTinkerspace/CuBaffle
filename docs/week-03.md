# Week 3: Deployment Mechanism Trade Study

**Goal this week:** Find the perfect deployment mechanism for the deployable optical baffle.

## What we did

- Conducted a formal trade study evaluating six different candidate mechanisms.
- Looked at traditional aerospace approaches, such as using a torsion spring to store deployment energy alongside a burn-wire hold-down release mechanism (HDRM).
- Compared those against more prototype-friendly mechanical solutions, like servo-driven string releases, 3-stage side screws, and direct servo arms.
- Scored each mechanism across 10 weighted parameters, (Note: The full scoring matrix and parameter breakdown is uploaded as a separate Trade Study document in the repo)

## Problems and blockers

- A true flight ready system, like the torsion spring with a burn-wire release, is incredibly compact and requires very low electrical energy. However, the burn-wire is effectively a one-time release. Having to replace the melted wire and re-tension the system for every single test cycle

## Decisions

- For the Ground Demonstrator: I selected Mechanism 6: Direct Servo Arm. This setup will use a dual-servo slotted lever (Scotch Yoke) system to physically push the baffle open and pull it closed.
- For a Future Flight Model: I concluded that Mechanism 2 (Torsion Spring + Servo-Driven Pin-Puller) or Mechanism 1 (Burn-Wire Release) would be the actual choices for space.

## Next week

- Move from theory to physical form factor. I need to understand press-fit clearances for the sliding tubes, figure out the actual dimensions to keep this within the 1U constraints etc.

