# Ezra Prototype Build Plan

Source note captured from the Companion prototype BOM. Prices and vendors are planning estimates, not live procurement quotes.

## Current CAD Direction

- Blender remains the fast exterior-form tool for the skip-stone surface, glow, Corian material read, and hand-feel iteration.
- Onshape should become the engineering source once the exterior is frozen enough to package real components.
- The BOM below should drive the first Onshape internal-layout pass: battery, CM4 carrier, LTE module, sensor boards, LEDs, haptics, thermal module, antennas, USB-C, gasket logic, and service access.

## Onshape Translation Note

Create an `Ezra_Internal_Packaging_v1` Onshape assembly once the exterior shell is stable. Start with simplified bounding volumes before detailed parts:

- `Battery_Main_4000_Prototype`: largest central mass, single-cell LiPo placeholder.
- `PCB_CM4_IO_Carrier`: rectangular carrier for Raspberry Pi CM4 plus IO board.
- `Module_Coral_USB_TPU`: secondary compute block near CM4.
- `Module_LTE_EC21_MiniPCIe`: modem block with antenna keep-out along shell perimeter.
- `Sensor_PPG_MAX30102_Array`: underside biometric island aligned to shell contact zone.
- `Sensor_EDA_AD5940`: conductive contact interface near thumb/finger zones.
- `Sensor_Air_SEN55`: seam-integrated vent path and air chamber.
- `Light_Flood_XHP50`: thermal path, reflector/optic, and Corian diffusion zone.
- `Light_UVA_NCSU334A`: side-shielded aperture with visible-cut filter.
- `Haptic_LRA_Array`: multiple actuator zones for thumb, palm, edges, and utility cues.
- `Thermal_TEC_20x20`: palm warmth zone with graphite spreader and thermal isolation.
- `Power_USB_C_BQ25895`: bottom service/charge path with gasket.

Created Onshape entry points in document `Codex_Diagnostic_Test`:

| Element | Type | Element ID | Purpose |
|---|---|---|---|
| `Ezra_BOM_Packaging_Placeholders_v1` | Part Studio | `d1355228e9eb178ab2b6ecdc` | Placeholder geometry and imported/vendor reference parts. |
| `Ezra_Internal_Packaging_BOM_v1` | Assembly | `be2dc958b8a119b3730466be` | Internal packaging assembly driven by the BOM. |

## Onshape Off-The-Shelf CAD Search

The Onshape MCP can search public Onshape documents and inspect/export part studios. It does not currently expose a direct derive/insert/import-into-this-document command, so these are candidate source documents to open manually in Onshape or export/import through a follow-up workflow.

| BOM Item | Onshape Search Result | Document ID | Notes |
|---|---|---|---|
| Raspberry Pi CM4 | `Raspberry Pi CM4` | `ae9d25e0db89ab906fc1fc44` | Strong candidate. Contains `Raspberry-Pi-CM4` Part Studio and STEP blob. |
| Raspberry Pi CM4 IO Board | `Raspberry PI IO board` | `0256854bfb4471139c1d7c6e` | Strong candidate for prototype carrier envelope. |
| MAX30102 | `MAX30102.SLDPRT` | `2b6a382b6096799f0e36eca2` | Strong candidate for PPG module/package reference. |
| Quectel EC21 | `Quectel EC21-AUTL.step` | `4b3c55a5fd12cfabc2584409` | Strong candidate for LTE module. |
| Sensirion SEN55 | `Sensirion SEN55 SEN5x Duct - Mechanical_Design-In_Example_Truncated` | `6846ed48a47e5b526f6cd8d3` | Useful for airflow/ducting, not necessarily bare module. |
| DRV2605L | `DRV2605L` | `00c73188beed332d03150c4e` | Candidate haptic driver board/package. |
| 10 mm LRA coin motor | `10mm Coin Motor Vibration` | `65e9de9b05d13340af12d902` | Strong candidate for haptic actuator envelope. |
| MAX98357A | `MAX98357A` | `7c0c1710348a5cfc73e3e0b8` | Candidate I2S amp board/package. |
| Cree XHP50 | `LED's` | `0ab29e3e7fa40ed86d333bf0` | Weak candidate; verify package before use. |
| BQ25895 | `librem-5.step` | `a7a767c02eb208051f59750e` | Weak candidate; likely embedded in a phone assembly, not standalone eval board. |
| USB-C breakout | `pico` | `f6a1da4123fb6da728473368` | Weak candidate; use only if connector geometry is reusable. |
| 20x20 Peltier TEC | No good direct result | N/A | Use bounding box until vendor STEP is sourced. |
| LiPo 4000 mAh | No reliable direct result | N/A | Use actual supplier dimensions as bounding box. |

Recommendation: pull exact CAD for the high-confidence modules first: CM4, CM4 IO board, Quectel EC21, MAX30102, SEN55, LRA coin motor, and USB-C connector. Represent batteries, wires, gaskets, Corian shell clearances, and thermal pads as custom Onshape placeholders.

## Prototype Timeline

| Phase | Scope | Timing |
|---|---|---|
| 01 | Order demo-critical parts | This week |
| 02 | Board bring-up and shell fabrication | Weeks 2-3 |
| 03 | Software stack | Weeks 2-4 |
| 04 | Investor demo ready | Week 5 |

## BOM Summary

| Category | Component | Qty | Est. Price | Priority | CAD Packaging Notes |
|---|---:|---:|---:|---|---|
| Compute | Raspberry Pi CM4, 4GB RAM, 32GB eMMC, WiFi | 1 | $75 | P1 | Main processor volume. |
| Compute | CM4 IO Board / full breakout carrier | 1 | $30 | P1 | Prototype carrier, likely larger than production board. |
| Compute | Coral USB Accelerator / Edge TPU | 1 | $60 | P2 | Thermal and USB routing allowance. |
| Cellular | Quectel EC21 Mini PCIe LTE Cat-1 Module | 1 | $35 | P1 | Needs SIM access and RF keep-out. |
| Cellular | T-Mobile prepaid SIM, IoT/data/voice | 2 | $20 | P1 | Procurement item, no CAD except SIM slot. |
| Cellular | LTE adhesive flex antenna, 700-2700 MHz | 1 | $12 | P2 | Perimeter antenna zone clear of metal. |
| Biometric | MAX30102 breakout, PPG / SpO2 / HR | 2 | $20 | P1 | Underside optical window and light pipe. |
| Biometric | AD5940 eval board, EDA / stress | 1 | $85 | P2 | Conductive ring/contact routing. |
| Biometric | Bosch BMP390 breakout, pressure/temperature | 1 | $10 | P2 | Vent path to environment. |
| Biometric | Infineon SLB 9670 TPM 2.0 module | 1 | $18 | P2 | Secure element near main PCB. |
| Environmental | Sensirion SEN55, PM2.5 / VOC / temp / humidity | 1 | $45 | P2 | Airflow chamber and waterproof membrane path. |
| Environmental | ST VL53L5CX ToF 8x8 depth array | 1 | $15 | P3 | Hidden optical aperture if retained. |
| Haptic/Thermal | TI DRV2605L haptic driver breakout | 2 | $20 | P1 | Driver board near actuator harness. |
| Haptic/Thermal | 10 mm coin LRA haptic actuators | 4 | $16 | P1 | Thumb, palm, left edge, right edge zones. |
| Haptic/Thermal | 20x20 mm Peltier TEC element | 1 | $8 | P1 | Palm warmth zone with thermal spreader. |
| Haptic/Thermal | TI DRV8833 dual H-bridge breakout | 1 | $5 | P1 | TEC driver and heat/cool direction control. |
| Light/UV | Cree XHP50.3 COB LED, warm white / 5000K | 1 | $8 | P1 | Floodlight thermal path and diffuser zone. |
| Light/UV | Ledil ANGIE-S TIR optic | 1 | $6 | P2 | Directional torch optic volume. |
| Light/UV | TI TPS92515 LED driver eval board | 1 | $25 | P2 | Constant-current LED driver. |
| Light/UV | Nichia NCSU334A UV-A LED, 365 nm | 2 | $14 | P1 | Shielded side aperture and baffle. |
| Light/UV | 365 nm UV-pass visible-cut filter | 1 | $18 | P2 | Aperture/filter stack. |
| Light/UV | Tunable white LED pair, 1800K + 5500K | 1 | $12 | P3 | Circadian ambient light zone. |
| Voice | Knowles SPH0645LM4H MEMS microphone breakout | 2 | $20 | P1 | Hidden microphone pores and acoustic channels. |
| Voice | MAX98357A I2S amplifier breakout + speaker | 1 | $15 | P1 | Speaker cavity and acoustic slit. |
| Power | TI BQ25895 USB-C charger + power path eval board | 1 | $49 | P1 | Charger board, battery path, USB-C route. |
| Power | 4000 mAh 3.7 V single-cell LiPo battery | 1 | $30 | P1 | Largest internal component in prototype. |
| Power | USB-C breakout board, 5 V power + data | 1 | $8 | P2 | Bottom gasketed port. |
| Shell | Corian sheet, white/Arctic, 12 mm | 1 | $40 | P2 | Prototype shell stock. |
| Shell | CNC machining: shell body + sensor array drilling | 1 | $200 | P2 | Include extra shells for breakage. |
| IP | USPTO provisional filing fee | 1 | $320 | P1 | Legal/procurement item, not CAD. |

## Demo Critical Path

The demo-critical hardware is CM4 + carrier, LTE, PPG, haptics, thermal, primary light, microphone/speaker, power, and shell. Environmental sensing, depth sensing, and tunable ambient LEDs can remain additive until the main interaction loop works.

## Investor Demo Moments

| Moment | Behavior | Hardware Dependency |
|---|---|---|
| Hand authentication | PPG identifies owner in roughly 4 seconds. | MAX30102, TPM, software model |
| Mom reaches out | Warmth plus amber haptic pulse. | LTE, LRA, TEC, light channel |
| Voice + memory | Voice query answered from structured memory. | CM4, mic, speaker, LLM stack |
| UV sweep | Surface contamination fluoresces under UV-A. | UV-A LEDs, filter, baffle |
| Live call | Voice command places cellular/WhatsApp call. | LTE, Android stack, mic/speaker |

## Patent Note

Potential provisional-claim themes:

- Continuous passive PPG biometric authentication on a screenless handheld companion device.
- PPG-gated FIDO2/WebAuthn passkey signing.
- Live PPG session continuity that closes on loss of biometric contact.
- Presence-triggered PPG activation via proximity/depth sensing.
- PPG plus voice dual-factor authentication without screen, camera, or fingerprint surface.
- UV-A fluorescence inspection integrated into a screenless personal device.
