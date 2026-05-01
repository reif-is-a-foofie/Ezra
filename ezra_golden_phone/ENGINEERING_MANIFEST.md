# Ezra Production Concept Manifest

## Master Variables

| Variable | Value |
|----------|-------|
| Length | 116 mm |
| Width tail | 64 mm |
| Width head | 60 mm visual leading taper |
| Center thickness | 15 mm |
| Edge thickness | 5.5 mm visual taper |
| Top shell wall | TBD after shell split |
| Bottom shell wall | TBD after shell split |
| Weight target | 165 g prototype target |
| Crown offset | 71.7 mm from trailing end / 13.7 mm ahead of center |
| Thumb side | stronger right-thumb shelf / concavity |
| Finger side | continuous rounder sweep |

## Sacred Geometry Package

| Rule | Value |
|------|-------|
| Governing datum | `B = 64 mm` palm short axis |
| φ | `1.6180339887` |
| Body ratio | `A/B = 116/64 = 1.8125` |
| Superellipse | Lamé exponent `n = 2.5` |
| Crown point | `A/φ = 71.7 mm` from trailing end |
| Golden gnomon feet | Front `(43,0)`, rear left `(-20,-20)`, rear right `(-20,+20)` |
| Foot triangle | Base `40 mm`, legs `66.1 mm`, apex `35.2°` |
| Bottom light array | Wide flood, focused flashlight, wide flood, all `92 mm` long |
| UV-A underside | Two small inspection emitters near the trailing underside edge |
| Fibonacci spiral | Non-rendered construction guide only; shape should feel derived from a flattened nautilus, not display a spiral graphic |

## Tactile Asymmetry Rule

Create tactile asymmetry hidden inside visual symmetry. Orientation should be obvious in hand but subtle to the eye.

Head end:
slightly narrower, flashlight aperture, directional speaker, far-field mic bias.

Tail end:
slightly fuller, battery mass, PPG/biometric underside island.

Thumb side:
gentle flattened capacitive strip and squeeze zone.

Finger side:
rounder grip contour and softer wrap.

Top dome:
highest point shifted 5 mm rearward/tailward.

Underside:
contact patch biased so table resting angle aims light slightly outward/upward.

## Onshape Package

Primary document: `Codex_Diagnostic_Test`

Product assembly:
`Ezra_Product_Assembly_v1`

Exploded assembly:
`Ezra_Exploded_Technical_Assembly_v1`

Prototype BOM and procurement-driven packaging notes:
`ezra_golden_phone/PROTOTYPE_BUILD_PLAN.md`

Part Studios:

| Studio | Purpose |
|--------|---------|
| `Top_Shell_A` | KRION/Corian top shell envelope, seam strategy, internal rib/standoff intent |
| `Bottom_Shell_A` | flatter underside, contact patch logic, sapphire PPG recess |
| `Frame_Internal_Mg` | magnesium/glass-filled nylon chassis envelope |
| `Battery_Main_6000` | largest central mass, 82×45×9 mm pouch envelope |
| `PCB_Main_v1` | main logic board plus AI SoC/NPU and PMIC clusters |
| `Sensor_PPG_Module` | secondary sensor PCB, PPG package alignment |
| `Audio_System_Dual` | voice speaker chamber and directional edge speaker envelope |
| `Light_System_Optics` | COB flood MCPCB and TIR flashlight lens |
| `Haptic_System_LRA` | central LRA actuator envelope and elastomer cradle |
| `Thermal_Warmth_Module` | graphite spreader / palm warmth zone |
| `Connectivity_Antenna_Zones` | perimeter antenna keepout envelope |
| `Charging_USB_Qi_Module` | hidden Qi coil, magnet ring, USB-C strategy |
| `Environmental_Sensors_Vents` | seam-integrated vent manifold and waterproof membrane intent |

## Engineering Sanity Checks

- Battery remains the largest central component and biases mass toward the tail.
- Qi/magnet package is hidden; it must not become exterior design language.
- Thermal module contacts graphite spreader and lower rear shell zone.
- PPG sensor aligns to 12 mm sapphire underside island.
- Antenna keepout stays on perimeter and away from major metal masses.
- Speaker chamber volume is represented as a physical cavity, not just a grille.
- Venting uses seam-integrated micro-slots, not obvious holes.
- User-facing exterior remains screenless, buttonless, screwless, and camera-free.

## PPG Relationship Sensor

PPG is both identity and passive relationship sensing. Each natural pickup can become a low-friction wellness sample without requiring a watch, app, or ritual.

Signal families:
heart rate, HRV, recovery state, stress-load trends, sympathetic arousal, indirect sleep-debt indicators, circulation quality / cold-hand state, respiratory rhythm trends, and baseline drift.

Positioning constraint:
pattern intelligence and personal regulation only. Do not claim medical diagnosis, treatment, disease detection, or clinical accuracy without a regulated medical pathway.

## Product Scene Assemblies

| Scene | Onshape element ID | Intent |
|-------|--------------------|--------|
| `Ezra_Scene_Morning_Guidance` | `33a3eb97a8d03f4b2b933002` | Bedside pickup, soft glow, low-recovery coaching |
| `Ezra_Scene_PreMeeting_Calm` | `a2336167188af890deb331b7` | Elevated pulse while held, slow haptic breathing cadence |
| `Ezra_Scene_Evening_WindDown` | `262a42c2ed729bab77166748` | Warm amber bedside mode, sleep-window guidance |
| `Ezra_Scene_WalkPrompt` | `806f9729d9de121066534e79` | Midday sedentary pattern, subtle pulse prompt |
| `Ezra_Scene_Emotional_Recovery` | `2e2a42f345d9b77ae6e173cd` | Post-stress regulation, gentle warmth and voice guidance |
