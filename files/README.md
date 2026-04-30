# Ezra

**A screenless, voice-first companion device. Carved from mineral stone. Built for the person, not the feed.**

---

## What is Ezra?

Ezra is an AI-native communication and identity device that eliminates the screen entirely. It does not have a display. It does not run apps. It does not have a feed. It replaces the smartphone's core functions — calls, messages, navigation, reminders, ambient awareness — through voice, haptic feedback, thermal sensation, and light.

The physical body is milled from KRION mineral solid surface — the same material used in high-end architectural surfaces. It is dense, warm to the touch, and silent in the hand. The interaction is entirely through sound and sensation. You speak. It responds. You feel the call before you hear it.

Ezra is a product of Good Industries, a venture studio within The Good Project.

---

## The Case for Screenless

The smartphone is the most intimate object most people own. It is also the most adversarial. Every major platform that runs on it — social media, news, entertainment — is optimized to extract attention, not serve the user. The screen is the delivery mechanism for that extraction.

Removing the screen does not reduce capability. It changes the contract. Ezra does not serve advertisers. It serves one person.

The addressable market is not "people who want a dumb phone." It is people who want a capable device that does not work against them.

---

## Core Product Description

Ezra is a palm-sized object, roughly the dimensions of a large river stone, milled from KRION mineral composite. It contains no screen. The interface is entirely voice, haptic, thermal, and light.

**It makes and receives calls.** Voice-first, with a beamforming microphone array and a high-fidelity speaker tuned for speech intelligibility in noisy environments.

**It knows who you are.** Photoplethysmography (PPG) sensors embedded behind a sapphire window read the user's pulse waveform the moment they pick up the device. No passcode. No face unlock. Authentication is passive and biometric — the device recognizes you by your cardiovascular signature.

**It communicates through sensation.** A linear resonant actuator (LRA) delivers haptic patterns with medical-grade precision. A Peltier thermoelectric element provides warmth — a contact notification from a family member can be felt before the user consciously processes it.

**It illuminates.** A 1,200 lumen COB LED array with a TIR optic can flood a room or throw a 60-meter beam — functioning as both an ambient presence light and an emergency torch.

**It is sovereign.** No screen means no browser, no app store, no feed. The operating surface for third-party exploitation does not exist.

---

## Project Status

| Phase | Status |
|-------|--------|
| Concept & Specification | ✅ Complete |
| Investor Deck | ✅ Complete |
| Physical Shell Prototype | 🔄 In progress |
| Firmware (RPi CM4 base) | 🔄 In progress |
| PPG authentication implementation | 📋 Scoped |
| Voice stack (Whisper + LLM) | 📋 Scoped |
| Haptic pattern library | 📋 Scoped |
| Manufacturing partner selection | ⏳ Pending |

---

## Repository Structure

```
ezra/
├── README.md                    ← This file
├── SPEC.md                      ← Full hardware & software specification
├── docs/
│   ├── philosophy.md            ← Product philosophy and positioning
│   ├── prototype-guide.md       ← How to build the investor prototype
│   ├── ppg-authentication.md    ← PPG identity implementation notes
│   └── fido2-integration.md     ← Passkey / FIDO2 architecture
├── specs/
│   ├── hardware.md              ← Component specifications
│   ├── firmware.md              ← Software stack overview
│   └── haptic-language.md      ← Haptic pattern vocabulary
└── assets/
    ├── renders/                 ← Product visualization images
    └── diagrams/                ← Architecture and interaction diagrams
```

---

## Contact

Good Industries · A division of The Good Project  
[thegoodproject.net](https://thegoodproject.net)

---

*"The stone that the builders rejected has become the cornerstone." — Psalm 118:22*
