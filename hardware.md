# Ezra — Hardware Specification

**Version:** 0.3  
**Stage:** Pre-prototype (Investor Demo Build)

---

## Component Selection Table

### Compute

| Component | Part | Manufacturer | Notes |
|-----------|------|--------------|-------|
| System on Chip | CM4 (4GB RAM / 32GB eMMC) | Raspberry Pi Foundation | Prototype only; production target: custom ARM SoC |
| Security Element | SLB 9670 TPM 2.0 | Infineon | PPG template and FIDO2 key storage |
| I/O Expander | MCP23017 | Microchip | GPIO expansion for button inputs and LED control |

### Cellular & Wireless

| Component | Part | Manufacturer | Notes |
|-----------|------|--------------|-------|
| LTE Modem | EC25-A Mini PCIe | Quectel | Cat 4 LTE, North America bands |
| Antenna | FXP73 flex LTE | Taoglas | Embedded in chassis perimeter |
| WiFi / Bluetooth | Integrated | RPi Foundation | CM4 onboard 802.11ac + BT 5.0 |
| SIM Slot | Nano SIM + eSIM | — | Dual SIM support |

### Audio

| Component | Part | Manufacturer | Interface | Notes |
|-----------|------|--------------|-----------|-------|
| Speaker | GF0401 (2W, 4Ω, 40mm) | Dayton Audio | Analog | Tuned for 200Hz–8kHz voice |
| Amplifier | MAX98357A | Maxim | I2S | 3.2W Class D, filterless |
| MEMS Mic (×4) | SPH0645LM4H | Knowles | I2S | Golden-rectangle perimeter array, phi-derived spacing |
| DSP / Wake Word | TrulyHandsfree SDK | Sensory | SPI | Wake word "Ezra," always-on < 10mW |

### Biometric / Identity

| Component | Part | Manufacturer | Interface | Notes |
|-----------|------|--------------|-----------|-------|
| PPG Sensor | MAX30102 | Maxim/Analog Devices | I2C | Red 660nm + IR 880nm |
| Optical Window | Sapphire disc, 12mm × 1.5mm | Industrial optics supplier | — | < 2% loss at sensor wavelengths |
| Optical Adhesive | NOA61 UV adhesive | Norland | — | Window to sensor bonding |

### Passive Regulation Signals

The PPG subsystem is a continuous relationship sensor, not just an unlock mechanism. It should sample opportunistically on pickup and during natural palm contact, then feed local trend models for heart rate, HRV, recovery state, stress-load trend, sympathetic arousal, cold-hand/circulation state, respiratory rhythm trend, and baseline drift. This is product guidance data, not diagnostic data.

Regulatory constraint: do not claim medical diagnosis, disease detection, treatment, or clinical accuracy unless Ezra enters a formal regulated medical pathway. Default positioning is pattern intelligence and personal regulation.

### Haptic

| Component | Part | Manufacturer | Interface | Notes |
|-----------|------|--------------|-----------|-------|
| Actuator | L5 LRA | Lofelt | — | ±3g peak force, 50–300Hz |
| Driver | DRV2605L | Texas Instruments | I2C | Arbitrary waveform RAM |
| Isolation | Sorbothane 40 duro | Sorbothane | — | Actuator mount isolation |

### Thermal (Warmth)

| Component | Part | Manufacturer | Notes |
|-----------|------|--------------|-------|
| Thermoelectric element | Thin thermal module / resistive warming plate | TBD | Production target for 21mm crowned body with 8mm edge thickness |
| Demo Peltier Element | TEC1-12706 | Generic | 40×40mm, 6A max, 51W; benchtop/investor demo only |
| MOSFET Driver | IRL3803 | Vishay | PWM control via CM4 GPIO |
| Heat Spreader | 1mm copper sheet, 50×40mm | McMaster-Carr | Hot side to chassis mass |
| Thermal Interface | Fujipoly XR-m (3 W/mK) | Fujipoly | Element to spreader |

### Illumination

| Component | Part | Manufacturer | Notes |
|-----------|------|--------------|-------|
| COB LED Array | BXRE-27G1000-C-73 (1,200 lm) | Bridgelux | Main flood/beam element |
| TIR Optic | TIR-T-H-10 (10° beam) | LEDiL | 60m beam throw |
| LED Driver | AL8861 | Diodes Inc. | Constant current, PWM dimming |
| Ambient Ring | SK6812 RGBW, 5mm, ×8 | Worldsemi | Notification color language |

### Power

| Component | Part | Manufacturer | Notes |
|-----------|------|--------------|-------|
| Battery | Custom Li-ion pouch, target 5,500–6,500mAh equivalent geometry | TBD | Largest central internal component; conformal or stacked pouch layout under crowned shell |
| Charging IC | BQ25895 | Texas Instruments | USB-C PD, 18W input |
| Wireless charging receiver | Qi2/MagSafe-compatible receiver module | TBD | Hidden centered rear coil; validate certification path with WPC |
| Magnetic alignment ring | N52 magnet ring array | TBD | Hidden under rear shell, sized for common phone magnetic charger puck alignment |
| USB-C Connector | HRO TYPE-C-31-M-17 | HRO | IP54 rated |
| Fuel Gauge | MAX17048 | Maxim | 1% accuracy SoC estimation |
| DC-DC (5V rail) | TPS62133 | Texas Instruments | CM4 power supply |
| DC-DC (3.3V rail) | AP2112K-3.3 | Diodes Inc. | Sensor power rail |

---

## Power Budget (Estimated)

| Subsystem | Active (mA @ 3.7V) | Standby (mA) |
|-----------|-------------------|--------------|
| CM4 (idle) | 400 | 80 |
| CM4 (voice processing) | 900 | — |
| LTE Modem (connected) | 350 | 15 |
| Audio (playback) | 180 | 2 |
| PPG sensor (active) | 5 | 0.7 |
| LRA (active) | 200 | 0 |
| Peltier (active, 50% PWM) | 3,000 | 0 |
| COB LED (max) | 1,000 | 0 |
| Misc (MCUs, sensors) | 30 | 8 |

**Typical use (voice + calls, no warmth/LED):** ~1,800mA average → 6,000mAh / 1,800mA ≈ ~3.3 hours of active-heavy use  
**Standby (LTE connected, PPG monitoring):** ~110mA → 6,000mAh / 110mA ≈ ~54 hours

---

## Thermal Constraints

The benchtop TEC1-12706 draws up to 22W (6A × 3.7V) at full duty cycle and is too bulky for the phone-scale enclosure. Production hardware needs a thin thermal module or resistive warming plate sized for burst warmth notifications (3–10 seconds), coupled to the palm-side shell through a graphite spreader. The chassis and mineral shell act as thermal reservoirs.

**Design constraint:** Limit Peltier duty cycle to 30-second maximum per activation. Software-enforced cooldown of 60 seconds between activations to prevent thermal accumulation.

---

## PCB Architecture

The device uses three PCBs:

1. **Main board:** CM4 carrier, LTE modem, power management, USB-C, battery connectors
2. **Sensor board:** MAX30102, DRV2605L, MCP23017, MAX17048, ambient LED ring
3. **Audio board:** MEMS mic array, MAX98357A, speaker connector

Boards connect via FFC (flat flexible cable) with ZIF connectors. This allows sensor and audio boards to be positioned independently of the main board geometry.

---

## Mechanical Interface Points

| Feature | Location | Tolerance |
|---------|----------|-----------|
| Speaker aperture | Upper face center | ±0.3mm |
| Sensor window | Lower face center | ±0.1mm (optical alignment critical) |
| Qi receiver coil | Rear center, hidden behind shell | ±0.5mm |
| Magnetic alignment ring | Rear center around coil, hidden behind shell | ±0.5mm |
| USB-C port | Lower edge | ±0.2mm |
| Internal glow / ambient light pipe | Perimeter groove or thinned mineral window | ±0.5mm |
| Peltier contact zone | Lower rear face | ±1mm |
| Battery access (service) | None (sealed) | — |

## Mechanical Envelope

| Parameter | Target |
|-----------|--------|
| Length | 108mm |
| Tail width | 66mm |
| Head width | 63mm |
| Center thickness | 21mm |
| Edge thickness | 8mm |
| Top shell wall | 3.2mm |
| Bottom shell wall | 2.8mm |
| Mass target | 210g |

The exterior must carry subtle tactile asymmetry: narrower head for flashlight/directional speaker/mic orientation, fuller tail for battery and biometric mass, a shallower thumb-side sweep, rounder finger-side squeeze contour, rearward crown offset of roughly 5mm, and a biased underside contact patch. The asymmetry should be felt more than seen.

---

*Hardware spec current as of April 2026. Prototype build may substitute components based on availability.*
