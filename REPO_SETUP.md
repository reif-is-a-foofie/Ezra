# Ezra — Repository Metadata

## GitHub Repository Settings

**Name:** `ezra`  
**Description:** Screenless AI companion device. Voice, haptic, and thermal interface. Milled from mineral stone.  
**Website:** https://thegoodproject.net  
**Topics:** `hardware`, `voice-interface`, `screenless`, `haptic`, `iot`, `raspberry-pi`, `embedded`, `fido2`, `ppg`, `biometrics`, `ai`, `llm`

## License

This project is currently **proprietary / all rights reserved** during the specification and prototype phase.

A decision on open-source licensing (likely Apache 2.0 for firmware, proprietary for hardware design files) will be made prior to any public prototype release.

## Visibility

Set to **Private** until provisional patent filing is complete.

Make **Public** after:
1. Provisional patent filed (PPG authentication + screenless FIDO2 architecture)
2. First investor prototype complete
3. Legal review of IP disclosure implications

---

## Repo Structure (Final)

```
ezra/
├── README.md
├── SPEC.md
├── CONTRIBUTING.md
├── LICENSE
├── docs/
│   ├── philosophy.md
│   ├── prototype-guide.md
│   ├── ppg-authentication.md
│   └── fido2-integration.md
├── specs/
│   ├── hardware.md
│   ├── firmware.md
│   └── haptic-language.md
├── firmware/               ← (pending)
│   ├── services/
│   │   ├── voice_pipeline.py
│   │   ├── identity_service.py
│   │   ├── haptic_service.py
│   │   ├── thermal_service.py
│   │   ├── light_service.py
│   │   └── minion_context.py
│   ├── drivers/
│   │   ├── max30102.py
│   │   ├── drv2605l.py
│   │   └── quectel_ec25.py
│   ├── patterns/
│   │   └── haptic_library.json
│   └── requirements.txt
├── hardware/               ← (pending)
│   ├── kicad/
│   └── mechanical/
└── assets/
    ├── renders/
    └── diagrams/
```
