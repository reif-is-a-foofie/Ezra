# Contributing to Ezra

Ezra is a hardware product in early specification and prototype phase. Contributions are welcome in the following areas:

## Areas Open for Contribution

### Firmware
- Voice pipeline implementation (Whisper + Claude API integration)
- PPG authentication feature extraction algorithms
- Haptic waveform design and pattern library
- FIDO2 authenticator implementation on CM4

### Hardware
- PCB design improvements (KiCad preferred)
- Thermal modeling of Peltier integration
- Acoustic chamber optimization for the speaker
- Alternative form factor explorations

### Documentation
- Corrections and clarifications to hardware specs
- Additional prototype build guides
- Regulatory documentation (FCC, CE)

## What We Are Not Building

Ezra does not have:
- A browser
- An app store
- A social media client
- Any advertising integration

Contributions that add these capabilities will not be accepted.

## Development Environment

Prototype firmware targets Raspberry Pi OS Lite (Debian Bookworm, 64-bit, headless). All firmware is written in Python 3.11+.

```bash
# Clone the repo
git clone https://github.com/[org]/ezra
cd ezra

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/
```

## Code Style

- Python: Black formatter, 88-character line length
- Commit messages: Conventional Commits format
- Documentation: Markdown, present tense

## Reporting Issues

Use GitHub Issues. For hardware issues, include:
- Component part number
- Failure mode and conditions
- Oscilloscope captures or log output if available

For firmware issues, include:
- OS version (`uname -a`)
- Python version (`python --version`)
- Full traceback

---

*This is a pre-commercial research project. No warranties expressed or implied.*
