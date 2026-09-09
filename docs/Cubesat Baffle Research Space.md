
> [!Open Questions ] Open Questions 
> 1. What is a cubesat and a optical baffle?
> 2. What optical design to use for the protoype?
> 	Is there exitng designs to replicate?
> 3. What is the form factor that I am going to work with?
> 4. Which deployment mechanism?
> 	Why?
> 	How?
> 5. Which Verification mechanism?
> 	Why?
> 	How?
> 6. An overview of the electronics section
> 	What electronics/electrical componentns are needed?
> 7. What would be the software work in the software work?
> 	Workflow
> 	Mandatary essentals 

Note: Some lines or Paragraphs have been copied from the reference materials as it is. 

| Name                      | Link                                                                              |
| ------------------------- | --------------------------------------------------------------------------------- |
| Cubesat + deployer basics | https://www.eoportal.org/other-space-activities/cubesat-concept#advanced-features |
| Cubesat.org               | https://www.cubesat.org/cubesatinfo                                               |
| Refernce research paper   | https://www.sciencedirect.com/science/article/pii/S0273117723008931               |


## What is a CubeSat?

A **CubeSat** is a standardized class of miniaturized satellites (originally developed as a picosatellite standard) designed to lower the cost and development time of space missions.

- **Origins & Purpose:** Initiated in 1999 by Robert J. Twiggs at Stanford University (SSDL) in collaboration with California Polytechnic State University (Cal Poly), it was created to give universities a low-cost, quick-turnaround framework for hands-on student training and technology demonstrations using commercial off-the-shelf (COTS) components.

- **The Standard "Unit" (1U):** The baseline form factor is a **1U**, defined as a **10 cm × 10 cm × 10 cm** cube with a maximum mass budget typically limited to **1 kg** (though larger or updated mass allowances exist depending on deployer standards).
### Design (Cubesat)

Dimensions mentioned in u, I u = 10cm*10cm*10cm, max mass for i u = 1.33kg

Since nearly all CubeSats are 10 cm × 10 cm (3.9 in × 3.9 in) (regardless of length) they can all be launched and deployed using a common deployment system called a Poly-PicoSatellite Orbital Deployer (P-POD), developed and built by Cal Poly**

No electronics [form factors](https://en.wikipedia.org/wiki/Computer_form_factor "Computer form factor") or communications protocols are specified or required by the CubeSat Design Specification, but COTS hardware has consistently used certain features which many treat as standards in CubeSat electronics. Most COTS and custom designed electronics fit the form of [PC/104](https://en.wikipedia.org/wiki/PC/104 "PC/104"), which was not designed for CubeSats but presents a 90 mm × 96 mm (3.5 in × 3.8 in) profile that allows most of the spacecraft's volume to be occupied.

Care must be taken in electronics selection to ensure the devices can tolerate the radiation present. For very [low Earth orbits](https://en.wikipedia.org/wiki/Low_Earth_orbit "Low Earth orbit") (LEO) in which atmospheric reentry would occur in just days or weeks, [radiation](https://en.wikipedia.org/wiki/Radiation "Radiation") can largely be ignored and standard consumer grade electronics may be used. Consumer electronic devices can survive LEO radiation for that time as the chance of a [single event upset](https://en.wikipedia.org/wiki/Single_event_upset) (SEU) is very low. Spacecraft in a sustained low Earth orbit lasting months or years are at risk and only fly hardware designed for and tested in irradiated environments. Missions beyond low Earth orbit or which would remain in low Earth orbit for many years must use [radiation-hardened](https://en.wikipedia.org/wiki/Radiation_hardening "Radiation hardening") devices.[[30]](https://en.wikipedia.org/wiki/CubeSat#cite_note-30) Further considerations are made for operation in high vacuum due to the effects of [sublimation](https://en.wikipedia.org/wiki/Sublimation_\(phase_transition\) "Sublimation (phase transition)"), [outgassing](https://en.wikipedia.org/wiki/Outgassing "Outgassing"), and [metal whiskers](https://en.wikipedia.org/wiki/Whisker_\(metallurgy\) "Whisker (metallurgy)"), which may result in mission failure.[[31]](https://en.wikipedia.org/wiki/CubeSat#cite_note-31)

## Optical Baffles

On Earth observation satellites, star trackers, and space telescopes, an optical baffle is an extended shield (often a tube or cone) mounted around an optical aperture.

- **Primary Purpose:** To block **stray light** (off-axis light from the Sun, Earth, Moon, or spacecraft reflections) from directly hitting camera lenses, detectors, or mirrors.

- **Internal Vanes:** The interior of the baffle contains light-trapping rings or knife-edge ridges (vanes) coated in ultra-black, light-absorbent materials. These structures prevent stray light from bouncing into the focal plane.

- **Why It Matters:** Without a baffle, bright off-axis sources would cause optical glare, reduce contrast, or drown out faint targets (such as distant stars used by star trackers for attitude determination).

- **CubeSat Deployer Accommodation:** In small satellites, optical camera baffles often protrude beyond the satellite body; deployers like ISIPOD include cylindrical envelope extensions to accommodate them.


##  Background on optical baffles

The primary objective of an optical payload on a satellite is to image areas of interest on the Earth. **A baffle is necessary to attenuate stray light from the sun to improve the optical performance of the payload.** Similarly, for a [star tracker](https://www.sciencedirect.com/topics/earth-and-planetary-sciences/star-tracker), the objective is to observe stars within its field of view (FoV) and compare the pattern with a [star catalogue](https://www.sciencedirect.com/topics/earth-and-planetary-sciences/astronomical-catalog) for attitude estimation of the satellite. This requires the star tracker to block any stray light from the sun, Earth or the moon to be able to detect the apparent magnitude of stars within the FoV correctly. While payloads which point at Earth may usually not have baffles, a star tracker always requires a baffle, without which a star tracker will be blinded by the sun. **As observed in [Curtis (2022)](https://www.sciencedirect.com/science/article/pii/S0273117723008931#b0040), all star trackers have a baffle**, and as the aperture of the star tracker increases, the length of the baffle increases. The total length of the baffle dominates the size of larger high-performing star trackers.

**The primary inputs to the design of the baffle are the stray light exclusion angle, ’_F_’ number and the field of view (FoV) for the optical system.** The mechanical requirements on size and mass result in a constraint on the overall size of the baffle, defining the maximum length and diameter that can be accommodated, along with the mass of the baffle system. Often, mechanical constraints take precedence over the [optical design](https://www.sciencedirect.com/topics/engineering/optical-design) requirements to meet the system-level requirements. Stray light entering the baffle wall will be further attenuated by introducing vanes, increasing the number of internal reflections within the baffle. Optimizing the number of vanes, vane tip profiles, and absorptive coatings on the inner wall of the baffle will further improve stray [light attenuation](https://www.sciencedirect.com/topics/earth-and-planetary-sciences/light-attenuation) ([Breault, 1989](https://www.sciencedirect.com/science/article/pii/S0273117723008931#b0020)).


[[Optical Design for a Fixed Baffle]]
[[Optical Design for a Deployable Baffle]]


