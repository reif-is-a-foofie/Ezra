# Ezra — Full Product Specification

**Version:** 0.4 (Pre-prototype)  
**Status:** Specification phase  
**Owner:** Good Industries / The Good Project

---

## 1. Physical Form Factor

### 1.1 Dimensions & Weight

| Parameter | Target |
|-----------|--------|
| Length | 116 mm |
| Width | 64 mm palm datum, with subtly narrower leading/head end |
| Depth | 15 mm crowned center / 5.5 mm visual edge |
| Top shell wall | TBD after shell split; target 3.0-3.5 mm |
| Bottom shell wall | 2.5 mm at light-diffusion zones / 3.5 mm perimeter target |
| Weight | 165g prototype target |
| Form | Flattened nautilus / skip-stone profile with hidden tactile asymmetry |

The governing palm datum is the 64mm short axis. The current skip-stone body is 116mm long, giving A/B = 1.8125. This is intentionally longer than pure φ because the device needs pocket reach, bottom flood-light real estate, and a more athletic skipping-stone read. The form remains φ-influenced through crown placement, foot geometry, haptic placement, seam behavior, and construction logic.

The industrial design target is a translucent warm-white mineral skip stone: longer and thinner than expected, shallow crowned top face, aggressively tapered edges, and no visible screen, camera, buttons, screws, or top markings. The object should feel like a flattened nautilus shell worn into a river stone, not a phone slab or hockey puck.

Ezra uses tactile asymmetry hidden inside visual symmetry. The leading/head end is slightly narrower and faster. The trailing/tail end is calmer and slightly fuller. The right-hand thumb side has a subtle concavity/shelf, while the opposite side remains a smooth finger sweep. The crown peak is φ-derived at 71.7mm from the trailing end, 13.7mm ahead of true center.

Sacred-geometry construction rules:
- **φ:** 1.6180339887.
- **Palm datum:** B = 64mm.
- **Long axis:** A = 116mm.
- **Superellipse:** Lamé curve, n = 2.5.
- **Crown point:** A/φ = 71.7mm from trailing end.
- **Feet:** golden gnomon triangle at (43, 0), (-20, -20), (-20, +20) mm.
- **Foot triangle:** 40mm base, 66.1mm legs, apex angle 35.2°, visually approximating the 36°/72°/72° golden gnomon.
- **Fibonacci spiral:** construction guide only. The top should feel derived from a flattened nautilus spiral, but the spiral must not be lit, engraved, printed, or visible as graphics.

The weight is deliberate but no longer brick-like. The target is 165g: dense enough to feel premium and stable on its feet, light enough to pocket and handle as a personal object.

### 1.2 Material: KRION Mineral Solid Surface

KRION (manufactured by Porcelanosa Group) is a mineral composite of approximately 2/3 natural minerals (primarily aluminum trihydrate) bound by a high-performance acrylic resin. Properties relevant to Ezra:

- **Non-porous:** Does not harbor bacteria; hygienic for daily skin contact
- **Thermoformable:** Can be CNC milled and hand-finished to tight tolerances
- **Repairable:** Surface scratches can be sanded and re-polished
- **Thermal conductivity:** Moderate; works with rather than against the Peltier element
- **Available in matte white and mineral tones:** Consistent with the product's aesthetic language

Alternative: Corian (DuPont / Trinseo) is functionally similar and more widely available through fabricators in the US market.

### 1.2.1 Internal Glow

Ezra may use a low-output internal amber glow through thinned KRION/Corian or a hidden perimeter light pipe. This is not a display surface and must not resolve into icons, pixels, notification badges, or text. The glow is limited to ambient state, warmth/social presence, charging feedback, and quiet location/state signaling. Translucency must be validated against actual material samples because standard mineral solid surface is mostly opaque at normal wall thickness.

Visual target reference, May 2026: a warm translucent mineral pebble on a black surface, with a crystalline/alabaster Corian texture, softly glowing amber core, and a clean continuous amber perimeter seam. The edge glow should reflect subtly on the table. The top face remains visually pure: no Fibonacci line, no logo, no lens, no display, no obvious sensor, and no decorative mesh. The surface should read as natural crystalline mineral, like white onyx/alabaster/Corian, not plastic.

### 1.3 Sensor Window

A 12mm circular recess machined into the lower face of the device accepts a sapphire optical disc, flush-mounted and adhesively sealed. The MAX30102 pulse oximetry / heart rate sensor sits behind this window inside the chassis. Sapphire transmits at the wavelengths used by the MAX30102 (red 660nm, infrared 880nm) with minimal loss and is scratch-resistant at 9 Mohs.

From the exterior, this window reads as the device's focal point — an eye. It is the only element that interrupts the mineral surface.

---

## 2. Hardware Components

### 2.1 Compute

| Component | Specification |
|-----------|---------------|
| SoC | Raspberry Pi Compute Module 4 (CM4) |
| RAM | 4GB LPDDR4 |
| Storage | 32GB eMMC |
| OS | Raspberry Pi OS Lite (headless) |

The CM4 is chosen for prototype phase due to ecosystem maturity, available I/O, and Bluetooth/WiFi integration. Production hardware would target a custom ARM SoC (MediaTek, Qualcomm, or equivalent) to achieve target power envelope.

### 2.2 Cellular & Connectivity

| Component | Specification |
|-----------|---------------|
| LTE Modem | Quectel EC25 or equivalent Cat 4 LTE |
| WiFi / BT | CM4 integrated (802.11ac, BT 5.0) |
| SIM | Nano SIM + eSIM capability |

### 2.3 Audio

| Component | Specification |
|-----------|---------------|
| Speaker | 2W full-range driver, tuned for 200Hz–8kHz voice intelligibility |
| Microphone array | 4× MEMS microphones on golden-rectangle perimeter grid (beamforming) |
| DSP | Sensory TrulyHandsfree or equivalent wake-word / noise suppression |
| Wake word | "Ezra" (custom model) |

### 2.4 Identity — PPG Authentication and Relationship Sensing

| Component | Specification |
|-----------|---------------|
| Sensor | MaxLinear MAX30102 (or MAX30101) |
| Window | 12mm sapphire disc, 1.5mm thickness |
| Authentication time | < 4 seconds from pickup |
| False acceptance rate | Target < 0.1% |
| Implementation | On-device enrolled pulse waveform template; comparison via dedicated security element |

**Mechanism:** The MAX30102 emits red (660nm) and infrared (880nm) light through the sapphire window into the user's palm. Reflected light is captured by the photodiode array. The resulting photoplethysmography (PPG) waveform encodes cardiovascular features (peak morphology, inter-beat interval, diastolic/systolic ratio) that are unique to the individual. An enrolled template is stored in the security element. Authentication occurs passively on pickup — no deliberate gesture required.

**Security note:** PPG authentication is a physiological biometric. It cannot be replicated by a photograph or a recording. If a different person picks up the device, the waveform does not match, the session closes, and the device presents as inert.

PPG is not only a lock. Every pickup is also a passive wellness signal captured without asking the user to wear a watch, open an app, or perform a health ritual. Ezra uses ordinary handling as a low-friction sampling moment.

PPG-derived pattern intelligence may include heart rate, HRV, recovery state, stress load trends, sympathetic arousal, indirect sleep-debt indicators, circulation quality / cold-hand state, respiratory rhythm trends, and baseline drift over weeks or months. These outputs are treated as behavioral intelligence and personal regulation cues, not medical diagnosis.

Example guidance behaviors:
- Morning pickup: "Your recovery looks low today. Consider a lighter workout."
- Pre-meeting pickup: elevated pulse triggers two slow breath haptics.
- Late night pickup: warm amber light and a wind-down suggestion.
- Midday pickup: sedentary trend triggers a subtle walk prompt.
- Post-conflict pickup: lingering elevation triggers emotional recovery guidance.

The product distinction is deliberate: a phone can measure things; Ezra shepherds behavior without adding screen distraction.

### 2.5 FIDO2 / Passkey Integration

Ezra functions as a hardware FIDO2 authenticator. The CM4 runs a FIDO2 authenticator stack (e.g., python-fido2 or custom implementation) backed by an Infineon SLB 9670 TPM for secure key storage. The PPG verification result serves as the FIDO2 User Verification step, satisfying the UV flag required for passkey authentication.

This means Ezra can authenticate the user silently to any FIDO2-compliant service — Google, Apple, Microsoft, GitHub, PayPal — without a password, PIN, or explicit action beyond picking up the device.

### 2.6 Haptic System

| Component | Specification |
|-----------|---------------|
| Actuator | Lofelt L5 LRA (or equivalent high-fidelity LRA) |
| Driver | DRV2605L haptic driver IC |
| Capability | Arbitrary waveform playback; frequency range 50–300Hz |
| Integration | Bottom-center chassis mount for palm transmission |

**Haptic language** (see `specs/haptic-language.md` for full vocabulary):
- Single slow pulse: ambient notification
- Double pulse: incoming call
- Warmth + amber light: message from designated contact ("loved one" pattern)
- Continuous slow throb: navigation waypoint approaching
- Sharp triple: urgent alert

### 2.7 Thermal System

| Component | Specification |
|-----------|---------------|
| Element | Thin thermoelectric patch target; TEC1-12706 allowed for benchtop demo only |
| Driver | Custom PWM driver (0–100% duty cycle) |
| Heat sink | Copper spreader plate to chassis mass |
| Range | Ambient +0°C to +8°C surface temperature delta |
| Location | Lower third of device rear face |

The thermoelectric element enables warmth as a communication channel. A designated contact can trigger a warmth notification — the device surface temperature rises 4–6°C above ambient, detectable within 1–2 seconds of holding the device. This is not a gimmick; it activates a different sensory modality than vibration or sound, allowing the device to communicate without intruding on conversation or environment.

### 2.8 Light System

| Component | Specification |
|-----------|---------------|
| Bottom light array | Three 92mm linear COB bands under 2.5mm Corian diffusion layer |
| Left band | Wide flood, warm/cool white, broad work-surface illumination |
| Center band | Focused flashlight/throw band with linear prismatic/TIR optic |
| Right band | Wide flood, paired with left band for shadowless rectangular flood |
| Output target | 1,500-2,000 lm peak burst; lower sustained/emergency modes |
| UV-A inspection | Two shielded 365nm underside emitters with visible-cut filter target |
| Ambient mode | 0.6mm perimeter seam RGBW light pipe for notification/color language |
| Driver | Constant-current LED drivers with independent PWM per band |

The bottom face is a functional light platform, not an afterthought. In normal hand use the top remains the calm mineral face. When inverted or placed on its three feet, the underside provides multiple light modes: wide flood, focused flashlight beam, combined work light, low candle/bedside mode, emergency locator, and UV-A inspection. The three feet raise the bottom surface for stability, scratch protection, and thermal airflow.

### 2.9 Power

| Component | Specification |
|-----------|---------------|
| Battery | Custom Li-ion pouch, 5,500–6,500mAh equivalent geometry target |
| Charging | USB-C PD, 18W; Qi2/MagSafe-style magnetic wireless charging target |
| Wireless charging envelope | Hidden centered rear coil and magnet ring, sized for common phone magnetic charger alignment |
| Target runtime | 18–24 hours typical use |
| Emergency mode | 72-hour mode (voice + minimal haptic only) |

---

### 2.10 Mechanical Packaging Map

The screenless face is functional real estate. Primary zones:

| Zone | Allocation | Notes |
|------|------------|-------|
| Center rear | Qi2/MagSafe-style receiver coil and magnet alignment ring | Hidden packaging constraint only; do not expose as exterior ring geometry |
| Lower front/palm face | 12mm sapphire PPG eye | Optically isolated from internal glow and adhesive stack |
| Lower rear | 40×40mm thermal presence envelope | Prototype may use external/benchtop TEC; production needs thin thermoelectric patch |
| Upper face/edge | Speaker aperture or hidden acoustic mesh | Avoid direct conflict with charger/magnet ring |
| Perimeter grid | 4× MEMS microphones | Golden-rectangle four-point spacing |
| Perimeter groove | Diffuse amber light pipe / RGBW status glow | Low-resolution ambient signal only, not a display |
| Bottom light platform | Wide flood band / focused flashlight band / wide flood band | Underside only; do not contaminate top face visual purity |
| Bottom UV-A | Two 365nm inspection emitters | Shielded, filtered, and visually quiet when off |
| Bottom feet | Three silicone-capped Corian feet in golden gnomon layout | (43,0), (-20,-20), (-20,+20) mm from bottom center |
| Bottom short edge | USB-C | Sealed port or gasketed connector |
| Outer perimeter | LTE/WiFi/Bluetooth antennas | Maintain clearance from magnet ring and metal heat spreader |

---

## 3. Software Stack

### 3.1 Voice Pipeline

```
Microphone array → DSP (noise suppression + wake word) → Whisper ASR → LLM inference → TTS → Speaker
```

- **Wake word detection:** On-device, always-on, < 10mW
- **ASR:** OpenAI Whisper (small model, on-device) for offline capability; larger model via API when connected
- **LLM:** Claude API (via Anthropic) for reasoning, memory, and context; local fallback for offline operation
- **TTS:** Coqui TTS or ElevenLabs API; custom voice trained on approved samples
- **Latency target:** < 800ms from end of speech to start of response

### 3.2 Memory & Context (Minion Integration)

Ezra integrates with Minion, Good Industries' persistent AI identity layer. Minion maintains:

- Conversation history and semantic memory
- Contact relationship graph
- Calendar and task state
- Health trends derived from PPG data (resting heart rate, HRV, stress indicators)
- Location and routine patterns

All memory is stored on-device first; cloud sync is encrypted and user-controlled.

### 3.3 Communication

| Function | Implementation |
|----------|----------------|
| Calls | SIP over LTE; VOIP fallback |
| Messages | SMS via modem; Signal protocol for encrypted contacts |
| AI-mediated messaging | Voice → text → send; incoming text → TTS readback |
| Passive regulation | PPG trend + context → voice, warmth, haptic, or light guidance |

### 3.4 Navigation

Turn-by-turn navigation delivered via haptic and voice only. No visual map. The LRA fires approaching waypoints; voice announces turns. Emergency navigation works offline using cached OSM tiles.

---

## 4. Identity & Privacy Architecture

Ezra's privacy model is device-sovereign by default.

| Principle | Implementation |
|-----------|----------------|
| No cloud dependency | Core functions operate offline |
| No advertising | No ad SDK, no telemetry without consent |
| Biometric data stays on device | PPG templates never leave the security element |
| End-to-end encryption | All messages encrypted in transit |
| User owns their data | Full export at any time; no vendor lock |

The device does not have a browser. It does not have an app store. The attack surface for third-party data extraction is structurally minimal.

---

## 5. Manufacturing Notes

### 5.1 Shell Fabrication

KRION / Corian blocks are available from architectural distributors (Porcelanosa, local Corian dealers). A 130×80×25mm billet provides adequate material for the 116×64mm crowned skip-stone shell with wall stock. CNC milling to net shape, followed by hand-sanding to satin mineral finish. Interior dimensions must accommodate all components with vibration isolation foam between the LRA and the chassis wall, plus a centered rear wireless charging coil and magnet ring hidden behind the exterior surface. The bottom shell must include three golden-gnomon feet, a shallow underside dish, and a thinned light-diffusion zone over the flood/flashlight/UV optics.

### 5.2 Assembly

Internal chassis is an aluminum or PETG-printed tray holding all components. The mineral shell slides over and bonds with structural adhesive. No external fasteners — the device is intentionally non-serviceable by the user (sealed like AirPods).

### 5.3 Regulatory

Target certifications for commercial release: FCC Part 15 (USA), CE (EU), PTCRB (cellular). PPG authentication does not currently require FDA clearance for wellness use (it does for medical claims — Ezra makes none).

---

## 6. Prototype Bill of Materials (Investor Demo)

| Component | Source | Estimated Cost |
|-----------|--------|----------------|
| KRION/Corian billet (125×80×30mm) | Porcelanosa distributor / Corian fabricator | $60–120 |
| CNC milling (shell only) | Local CNC shop | $500–1,500 |
| Raspberry Pi CM4 (4GB/32GB) | DigiKey / Mouser | $75 |
| MAX30102 breakout | SparkFun / Adafruit | $25 |
| Sapphire optical disc (12mm) | Industrial optics supplier | $30–60 |
| Lofelt L5 LRA | Lofelt direct | $80 |
| DRV2605L driver board | Adafruit | $8 |
| Peltier TEC element | Amazon / DigiKey | $10 |
| COB LED + TIR optic | LED supplier | $25 |
| Speaker (2W, 40mm) | Parts Express | $12 |
| MEMS microphone array | DigiKey | $15 |
| Quectel EC25 LTE module | Quectel direct | $45 |
| Custom Li-ion pouch placeholder (6,000mAh class) | Battery supplier / prototype substitute | $40–80 |
| USB-C PD charging board | Adafruit | $15 |
| Misc (wiring, PCB, adhesive) | — | $100 |
| **Total** | | **~$1,000–2,200** |

Engineering time for prototype integration (one embedded engineer): 2–3 weeks at approximately $150–200/hour.

---

*Specification current as of April 2026. Subject to revision as prototype testing informs component selection.*
