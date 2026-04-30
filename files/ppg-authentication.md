# Ezra — PPG Authentication Implementation

## Overview

Photoplethysmography (PPG) authentication is the identity layer that makes Ezra sovereign to its owner. Unlike fingerprint scanners (which require a precise placement gesture) or facial recognition (which requires a screen and a camera), PPG authentication occurs passively the moment the device is held. The user does nothing. The device recognizes them.

---

## How PPG Works

A PPG sensor (the MAX30102 in Ezra's implementation) emits red (660nm) and infrared (880nm) light into tissue. The photodiode array captures the portion of that light reflected back. Because blood absorbs light at different rates depending on oxygenation and volume, each heartbeat produces a characteristic waveform in the reflected signal.

This waveform encodes features that are unique to the individual's cardiovascular anatomy:
- Peak morphology (shape of the systolic peak)
- Diastolic notch characteristics
- Pulse arrival time
- Inter-beat interval variability

These features are stable across time for a given individual and are substantially different between individuals. The discriminating power is sufficient for single-user authentication (one enrolled user vs. impostor) with false acceptance rates below 0.1%.

---

## Implementation in Ezra

### Hardware Path

```
User's palm → Sapphire window (12mm) → MAX30102 photodiode → I2C → CM4 → Security Element
```

The sapphire window (12mm diameter, 1.5mm thickness) transmits at both 660nm and 880nm with < 2% loss. The MAX30102 sits on the interior face of the window, secured with optical adhesive.

**KRION transmissivity:** KRION mineral solid surface does not transmit at these wavelengths at standard wall thickness. The sapphire window is mandatory — you cannot read PPG through the mineral body. This is why the window is recessed into the lower face of the device rather than reading through the shell.

### Enrollment

On first boot, the user holds the device for 30 seconds. The system captures 30 seconds of PPG data, extracts features, and stores a template in the Infineon SLB 9670 TPM (Trusted Platform Module). The template never leaves the security element.

The enrollment process runs 3× and averages the extracted template to improve robustness against normal physiological variability (exercise, temperature, posture).

### Authentication

On subsequent pickups:

1. MAX30102 detects contact (proximity sensor triggers on skin contact)
2. 4-second PPG acquisition begins
3. Feature extraction runs on CM4 (not in security element — only comparison occurs there)
4. Extracted features transmitted to TPM via secure channel
5. TPM compares against enrolled template using Euclidean distance in feature space
6. Match (distance below threshold) → session unlocked
7. No match → device remains locked; PPG acquisition retries for 10 seconds, then hibernates

**Target latency:** < 4 seconds from pickup to authenticated state.

### Session Management

Once authenticated, the session remains active while the device is in continuous contact with the user's hand. A 30-second gap in PPG signal closes the session. This prevents session hijacking from device theft.

**Shared device scenario:** If a second person picks up the device after the owner sets it down, the PPG waveform does not match. The session from the previous owner is already closed (30-second gap). The device presents as locked. No explicit action required from the owner.

---

## FIDO2 Integration

The PPG authentication result feeds into a FIDO2 authenticator stack running on the CM4. When a relying party (any FIDO2-compliant service) requests authentication:

1. Relying party sends challenge to Ezra via Bluetooth (CTAP2 protocol)
2. Ezra checks current PPG session status
   - If active (authenticated in last 30 seconds): proceed
   - If not active: request PPG re-authentication
3. TPM signs the challenge with the registered private key
4. Signed response returned to relying party
5. Authentication complete — UV (User Verification) flag set to true

This satisfies the FIDO2 User Verification requirement for passkey authentication. Ezra functions as a hardware security key equivalent to a YubiKey, with the difference that user verification is biometric and passive rather than explicit (button press).

**Supported platforms:** Any service implementing WebAuthn / FIDO2 passkeys. As of 2026, this includes Google, Apple, Microsoft, GitHub, Dropbox, PayPal, Coinbase, and most major enterprise identity providers.

---

## Patent Considerations

The combination of PPG-verified FIDO2 authentication on a screenless form factor is believed to be unoccupied in the current patent landscape. The specific claims worth filing:

1. Method for passive FIDO2 user verification using PPG waveform matching
2. Device architecture combining PPG authentication with screenless voice interface
3. Session management system using continuous PPG contact monitoring for security state

**Recommendation:** File provisional patent application before public disclosure of the authentication mechanism. The prototype build should follow the provisional filing.

---

## Limitations and Known Issues

**Environmental factors:** PPG signal quality degrades with cold hands (vasoconstriction reduces perfusion), intense exercise (motion artifact), and dry skin. Mitigation: signal quality threshold check before authentication attempt; retry prompts via haptic if signal quality insufficient.

**Enrollment stability:** Initial enrollment should be performed under resting conditions (seated, room temperature). The enrolled template may need periodic re-enrollment if the user's cardiovascular profile changes significantly (weight change, medication changes, recovery from illness).

**Identical twins:** PPG waveforms between identical twins have been shown to be more similar than random pairs but remain distinguishable in most cases. For the initial product, this edge case is not addressed.

**Spoofing:** PPG waveforms cannot be replicated from a photograph, recording, or 3D print. Unlike fingerprints, there is no known method to construct an artificial PPG signal that matches a specific individual without access to their actual cardiovascular system. This makes PPG intrinsically more spoof-resistant than optical fingerprint scanners.

---

## Reference Implementation

The prototype implementation uses:

- **MAX30102 library:** SparkFun Arduino MAX3010x library (adapted for Python/RPi)
- **Feature extraction:** SciPy signal processing (peak detection, interval analysis)
- **Template storage:** SLB 9670 TPM via tpm2-tools (Linux)
- **FIDO2 stack:** python-fido2 library (Yubico) adapted for custom authenticator

Source code for the reference implementation is in `/firmware/ppg/` (pending).

---

*Implementation notes current as of April 2026. Component selection subject to revision based on prototype testing.*
