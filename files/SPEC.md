# Ezra — Full Product Specification

**Version:** 0.3 (Pre-prototype)  
**Status:** Specification phase  
**Owner:** Good Industries / The Good Project

---

## 1. Physical Form Factor

### 1.1 Dimensions & Weight

| Parameter | Target |
|-----------|--------|
| Length | 110–120 mm |
| Width | 55–65 mm |
| Depth | 18–22 mm |
| Weight | 180–220g (intentionally substantial) |
| Form | Rounded river-stone profile, bilateral grip geometry |

The weight is a deliberate design decision. A device that feels dense and present does not feel disposable. The heft signals quality and longevity. Mass also functions as a thermal battery for the Peltier element.

### 1.2 Material: KRION Mineral Solid Surface

KRION (manufactured by Porcelanosa Group) is a mineral composite of approximately 2/3 natural minerals (primarily aluminum trihydrate) bound by a high-performance acrylic resin. Properties relevant to Ezra:

- **Non-porous:** Does not harbor bacteria; hygienic for daily skin contact
- **Thermoformable:** Can be CNC milled and hand-finished to tight tolerances
- **Repairable:** Surface scratches can be sanded and re-polished
- **Thermal conductivity:** Moderate; works with rather than against the Peltier element
- **Available in matte white and mineral tones:** Consistent with the product's aesthetic language

Alternative: Corian (DuPont / Trinseo) is functionally similar and more widely available through fabricators in the US market.

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
| Microphone array | 3× MEMS microphones in triangular array (beamforming) |
| DSP | Sensory TrulyHandsfree or equivalent wake-word / noise suppression |
| Wake word | "Ezra" (custom model) |

### 2.4 Identity — PPG Authentication

| Component | Specification |
|-----------|---------------|
| Sensor | MaxLinear MAX30102 (or MAX30101) |
| Window | 12mm sapphire disc, 1.5mm thickness |
| Authentication time | < 4 seconds from pickup |
| False acceptance rate | Target < 0.1% |
| Implementation | On-device enrolled pulse waveform template; comparison via dedicated security element |

**Mechanism:** The MAX30102 emits red (660nm) and infrared (880nm) light through the sapphire window into the user's palm. Reflected light is captured by the photodiode array. The resulting photoplethysmography (PPG) waveform encodes cardiovascular features (peak morphology, inter-beat interval, diastolic/systolic ratio) that are unique to the individual. An enrolled template is stored in the security element. Authentication occurs passively on pickup — no deliberate gesture required.

**Security note:** PPG authentication is a physiological biometric. It cannot be replicated by a photograph or a recording. If a different person picks up the device, the waveform does not match, the session closes, and the device presents as inert.

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
| Element | Peltier TEC1-12706 (40×40mm, 6A) |
| Driver | Custom PWM driver (0–100% duty cycle) |
| Heat sink | Copper spreader plate to chassis mass |
| Range | Ambient +0°C to +8°C surface temperature delta |
| Location | Lower third of device rear face |

The Peltier element enables warmth as a communication channel. A designated contact can trigger a warmth notification — the device surface temperature rises 4–6°C above ambient, detectable within 1–2 seconds of holding the device. This is not a gimmick; it activates a different sensory modality than vibration or sound, allowing the device to communicate without intruding on conversation or environment.

### 2.8 Light System

| Component | Specification |
|-----------|---------------|
| LED array | COB LED, 1,200 lm output |
| Optic | TIR (total internal reflection) optic, 10° spot |
| Range | 60-meter beam throw at 10° |
| Diffuse mode | 120° flood via diffuser panel |
| Ambient mode | Perimeter LED ring (RGB, 5mm) for notification color language |
| Driver | Constant-current LED driver with PWM dimming |

### 2.9 Power

| Component | Specification |
|-----------|---------------|
| Battery | 3,500mAh LiPo |
| Charging | USB-C PD, 18W |
| Target runtime | 18–24 hours typical use |
| Emergency mode | 72-hour mode (voice + minimal haptic only) |

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

KRION / Corian blocks are available from architectural distributors (Porcelanosa, local Corian dealers). A 110×65×25mm billet provides adequate material for the chassis with wall stock. CNC milling to net shape, followed by hand-sanding to 1200 grit and matte finish. Interior dimensions must accommodate all components with vibration isolation foam between the LRA and the chassis wall.

### 5.2 Assembly

Internal chassis is an aluminum or PETG-printed tray holding all components. The mineral shell slides over and bonds with structural adhesive. No external fasteners — the device is intentionally non-serviceable by the user (sealed like AirPods).

### 5.3 Regulatory

Target certifications for commercial release: FCC Part 15 (USA), CE (EU), PTCRB (cellular). PPG authentication does not currently require FDA clearance for wellness use (it does for medical claims — Ezra makes none).

---

## 6. Prototype Bill of Materials (Investor Demo)

| Component | Source | Estimated Cost |
|-----------|--------|----------------|
| KRION billet (110×65×25mm) | Porcelanosa distributor | $40–80 |
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
| LiPo battery (3,500mAh) | Adafruit | $20 |
| USB-C PD charging board | Adafruit | $15 |
| Misc (wiring, PCB, adhesive) | — | $100 |
| **Total** | | **~$1,000–2,200** |

Engineering time for prototype integration (one embedded engineer): 2–3 weeks at approximately $150–200/hour.

---

*Specification current as of April 2026. Subject to revision as prototype testing informs component selection.*
