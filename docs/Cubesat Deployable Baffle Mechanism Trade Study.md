
> [!NOTE] Objective
> Find the perfect deployment mechnism for a deplyable optical baffle.
> 1. Stows within 1U cubsesat dimensions
> 2. Able to deply the baffle to full extension
> 3. Able to build and testable with 5 working days 
> 4. Repeatable - must survie mulitple deployment cycles 

## Candidate Mechanisms

### 1. Torsion Spring + Burn-Wire Release
A torsion spring stores the deployment energy while a burn wire restrains the baffle in its stowed position. Activating the burn wire releases the baffle, resulting in a fast, essentially uncontrolled deployment. For repeatbale testing the burn wire must be replaced each iteration. 
### 2. Torsion Spring + Servo-Driven Pin Puller
The torsion spring provides deployment force while a servo retracts a mechanical pin to release the baffle. The system can be manually re-stowed and re-armed, making it suitable for repeated testing.
### 3. Torsion Spring + Solenoid Latch
Similar to Mechanism 2, but a solenoid operates the release latch instead of a servo-driven pin. It provides repeatable spring-driven deployment but does not provide deployment-speed control.
### 4. Torsion Spring + Servo-Driven String Release
A string connected to the baffle is controlled by a servo, which progressively releases the string during deployment. This allows the spring-driven deployment to be slowed and controlled, and the process can be reversed for stowing.
### 5. Three-Stage Screw Side Deployment
A three-stage screw mechanism is positioned along the sides of the baffle and driven by a servo/stepper motor. Extension of the mechanism pushes the baffle outward, allowing controlled and repeatable deployment and stowing.
### 6. Direct Servo Arm
A servo arm directly pushes the baffle between the stowed and deployed positions. It is mechanically simple, highly repeatable, and provides direct control over deployment speed.

- - -
# Comparison Parameters and Weightage

| Parameter                  | Weight | Reason                                |
| -------------------------- | -----: | ------------------------------------- |
| Buildability & testability |      5 | Must be achievable within 1 week      |
| Repeatability              |      5 | Must support repeated demo cycles     |
| Deployment-speed control   |      4 | Controlled motion is desirable        |
| Stowed volume              |      5 | Must fit within 1U formfactor         |
| Control simplicity         |      3 | Minimize electronics/firmware risk    |
| Visual/demo clarity        |      3 | Deployment should be clearly visible  |
| Cost & availability        |      2 | Parts must be obtainable quickly      |
| Safety                     |      2 | Avoid unnecessary hazards             |
| Energy consumption         |      4 | Important for flight relevance        |
| Mechanical complexity      |      4 | Lower complexity reduces failure risk |

Scores are from 1–5, where 5 is best for each parameter.

---

# Result
| Mechanism                | Buildability & testability | Repeatability | Deployment-speed control | Stowed volume | Control simplicity | Visual/demo clarity | Cost & availability | Safety | Energy consumption | Mechanical complexity | Weighted Score | Normalized Score |
| ------------------------ | -------------------------: | ------------: | -----------------------: | ------------: | -----------------: | ------------------: | ------------------: | -----: | -----------------: | --------------------: | -------------- | ---------------- |
| **1. Burn wire**         |                          2 |             1 |                        1 |             5 |                  5 |                   3 |                   5 |      3 |                  5 |                     5 | **124 / 185**  | **3.35**         |
| **2. Servo pin-puller**  |                          5 |             5 |                        1 |             4 |                  5 |                   3 |                   5 |      4 |                  4 |                     5 | **152 / 185**  | **4.11**         |
| **3. Solenoid latch**    |                          5 |             5 |                        1 |             4 |                  4 |                   3 |                   5 |      4 |                  2 |                     5 | **141 / 185**  | **3.81**         |
| **4. String release**    |                          3 |             5 |                        5 |             4 |                  2 |                   5 |                   5 |      5 |                  1 |                     2 | **133 / 185**  | **3.59**         |
| **5. Three-stage screw** |                          2 |             5 |                        5 |             3 |                  2 |                   5 |                   3 |      5 |                  2 |                     1 | **119 / 185**  | **3.22**         |
| **6. Direct servo arm**  |                          5 |             5 |                        5 |             5 |                  5 |                   5 |                   5 |      5 |                  3 |                     5 | **177 / 185**  | **4.78**         |
## Parameter Based Sub results
### Buildability & Testability

| Mechanism           | Score | Reason                                                               |
| ------------------- | ----: | -------------------------------------------------------------------- |
| 1. Burn wire        |     2 | Simple mechanism, but one-time release complicates repeated testing. |
| 2. Servo pin-puller |     5 | Simple, readily available components and easy resetting.             |
| 3. Solenoid latch   |     5 | Simple mechanism with readily available components.                  |
| 4. String release   |     3 | Requires careful string routing, tension and servo tuning.           |
| 5. Screw mechanism  |     2 | Multiple stages require fabrication, alignment and tuning.           |
| 6. Servo arm        |     5 | Simplest mechanism to fabricate and integrate.                       |
###  Repeatability 

| Mechanism           | Score | Reason                                              |
| ------------------- | ----: | --------------------------------------------------- |
| 1. Burn wire        |     1 | Release is effectively one-time.                    |
| 2. Servo pin-puller |     5 | Can be manually re-stowed and re-armed.             |
| 3. Solenoid latch   |     5 | Latch can be repeatedly engaged and released.       |
| 4. String release   |     5 | Can be repeatedly deployed and stowed.              |
| 5. Screw mechanism  |     5 | Motor provides repeatable extension and retraction. |
| 6. Servo arm        |     5 | Fully repeatable servo-controlled motion.           |
### Deployment-Speed Control

| Mechanism           | Score | Reason                                                 |
| ------------------- | ----: | ------------------------------------------------------ |
| 1. Burn wire        |     1 | Spring releases the baffle immediately.                |
| 2. Servo pin-puller |     1 | Servo controls only the release, not deployment speed. |
| 3. Solenoid latch   |     1 | Binary release with no speed control.                  |
| 4. String release   |     5 | Servo controls the rate of string release.             |
| 5. Screw mechanism  |     5 | Motor speed directly controls deployment speed.        |
| 6. Servo arm        |     5 | Servo speed can be controlled throughout deployment.   |
### 7. Stowed Volume

| Mechanism           | Score | Reason                                                        |
| ------------------- | ----: | ------------------------------------------------------------- |
| 1. Burn wire        |     5 | Compact and easy to package internally.                       |
| 2. Servo pin-puller |     4 | Compact but requires space for the servo and pin.             |
| 3. Solenoid latch   |     4 | Requires additional space for the solenoid.                   |
| 4. String release   |     4 | String routing and servo placement add packaging constraints. |
| 5. Screw mechanism  |     3 | Side mechanisms consume more internal volume.                 |
| 6. Servo arm        |     5 | Compact and easy to position near the baffle.                 |
### Control Simplicity

| Mechanism           | Score | Reason                                          |
| ------------------- | ----: | ----------------------------------------------- |
| 1. Burn wire        |     5 | Simple binary release.                          |
| 2. Servo pin-puller |     5 | Simple servo command.                           |
| 3. Solenoid latch   |     4 | Simple but requires solenoid power switching.   |
| 4. String release   |     2 | Requires controlled servo movement.             |
| 5. Screw mechanism  |     2 | Requires motor control and position management. |
| 6. Servo arm        |     5 | Standard servo positioning.                     |
### Visual/Demo Clarity

| Mechanism           | Score | Reason                                              |
| ------------------- | ----: | --------------------------------------------------- |
| 1. Burn wire        |     3 | Deployment is too fast to clearly observe.          |
| 2. Servo pin-puller |     3 | Clear movement but essentially instantaneous.       |
| 3. Solenoid latch   |     3 | Same limitation as the pin-puller.                  |
| 4. String release   |     5 | Controlled deployment is highly visible.            |
| 5. Screw mechanism  |     5 | Controlled mechanical extension is easy to observe. |
| 6. Servo arm        |     5 | Motion can be slowed and clearly demonstrated.      |
### Cost & Availability

| Mechanism           | Score | Reason                                                       |
| ------------------- | ----: | ------------------------------------------------------------ |
| 1. Burn wire        |     3 | Low component cost but lot of burn wires needed for testing. |
| 2. Servo pin-puller |     5 | Cheap and readily available components.                      |
| 3. Solenoid latch   |     5 | Solenoids and supporting components are readily available.   |
| 4. String release   |     5 | Uses inexpensive servo, string and basic hardware.           |
| 5. Screw mechanism  |     3 | Requires several mechanical/custom components.               |
| 6. Servo arm        |     5 | Very few inexpensive components required.                    |
### Safety

|Mechanism|Score|Reason|
|---|--:|---|
|1. Burn wire|3|Involves a heated release element.|
|2. Servo pin-puller|4|No thermal release mechanism.|
|3. Solenoid latch|4|Simple electrical actuation.|
|4. String release|5|Low-energy mechanical system.|
|5. Screw mechanism|5|Controlled mechanical actuation.|
|6. Servo arm|5|Simple low-energy mechanism.|
### Energy Consumption

|Mechanism|Score|Reason|
|---|--:|---|
|1. Burn wire|5|Very low electrical energy; spring provides deployment energy.|
|2. Servo pin-puller|4|Servo only operates the release mechanism.|
|3. Solenoid latch|2|Solenoid requires relatively high current during actuation.|
|4. String release|1|Servo must actively control deployment and stowing.|
|5. Screw mechanism|2|Motor actively drives the mechanism throughout motion.|
|6. Servo arm|3|Servo directly provides deployment torque.|
### Mechanical Complexity

| Mechanism           | Score | Reason                                                          |
| ------------------- | ----: | --------------------------------------------------------------- |
| 1. Burn wire        |     5 | Very few mechanical components.                                 |
| 2. Servo pin-puller |     5 | Simple spring, pin and servo arrangement.                       |
| 3. Solenoid latch   |     5 | Simple mechanical architecture.                                 |
| 4. String release   |     2 | Requires string routing, tension control and payout management. |
| 5. Screw mechanism  |     1 | Multiple stages, moving interfaces and alignment requirements.  |
| 6. Servo arm        |     5 | Very few moving parts.                                          |
- - -

# Conclusion

For the **ground demonstrator, Mechanism 6  Direct Servo Arm** is selected due to its simplicity, repeatability, and precise deployment-speed control.

For an **actual space-grade system, Mechanism 2 Torsion Spring + Servo-Driven Pin-Puller** a good option due to its simple, low-power, spring-driven deployment. **Mechanism 1  Burn-Wire Release** is also a strong flight candidate, offering an even simpler passive release with good resistance to shock and vibration.