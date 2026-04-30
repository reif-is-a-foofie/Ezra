# Ezra — Firmware & Software Stack

**Target platform:** Raspberry Pi CM4, Raspberry Pi OS Lite (Debian Bookworm, 64-bit, headless)  
**Primary language:** Python 3.11+  
**Architecture:** Service-oriented, ZeroMQ message bus

---

## System Architecture

```
┌─────────────────────────────────────────────────────┐
│                   EZRA FIRMWARE                      │
│                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │
│  │ Voice    │  │ Haptic   │  │ Identity         │  │
│  │ Pipeline │  │ Service  │  │ Service (PPG)    │  │
│  └────┬─────┘  └────┬─────┘  └────────┬─────────┘  │
│       │             │                 │             │
│  ┌────▼─────────────▼─────────────────▼─────────┐  │
│  │              ZeroMQ Message Bus               │  │
│  └────┬─────────────┬─────────────────┬─────────┘  │
│       │             │                 │             │
│  ┌────▼─────┐  ┌────▼─────┐  ┌────────▼─────────┐  │
│  │ Minion   │  │ Thermal  │  │ Light            │  │
│  │ Context  │  │ Service  │  │ Service          │  │
│  │ (Memory) │  │(Peltier) │  │ (LED/COB)        │  │
│  └──────────┘  └──────────┘  └──────────────────┘  │
│                                                     │
│  ┌─────────────────────────────────────────────┐    │
│  │         Cellular / Connectivity Manager     │    │
│  └─────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
```

All services communicate via ZeroMQ PUSH/PULL and PUB/SUB patterns. No service calls another directly — all inter-service communication goes through the message bus. This allows services to be developed and tested independently.

---

## Service Descriptions

### Voice Pipeline Service

**Responsibilities:** Wake word detection → ASR → LLM inference → TTS → audio output

**Stack:**
- Wake word: Sensory TrulyHandsfree SDK (always-on, < 10mW)
- ASR: `openai-whisper` (small model, on-device); whisper-large via API when connected
- LLM: Claude API (`claude-sonnet-*`) as primary; local `llama.cpp` (Phi-3 mini) as offline fallback
- TTS: Coqui TTS (on-device) or ElevenLabs API

**Key behaviors:**
- Wake word "Ezra" activates the pipeline
- Context window passed to LLM includes Minion memory snapshot (last 20 relevant items)
- Response streamed to TTS before full response is generated (reduces perceived latency)
- After 30 seconds of silence, pipeline returns to wake-word-listening state

**Configuration:**
```yaml
voice:
  wake_word: "ezra"
  asr_model: "whisper-small"
  asr_api_fallback: true
  llm_model: "claude-sonnet-4-20250514"
  llm_offline_fallback: "phi3-mini"
  tts_voice: "ezra-v1"  # custom trained voice
  tts_api_fallback: true
```

### Identity Service (PPG)

**Responsibilities:** Continuous PPG monitoring → session authentication → session management → FIDO2 interface

**Stack:**
- MAX30102 driver: custom Python via `smbus2`
- Feature extraction: `scipy.signal` (peak detection, interval analysis)
- Template comparison: custom implementation against TPM-stored template
- FIDO2: `python-fido2` (Yubico) adapted for custom authenticator
- TPM interface: `tpm2-tools` via subprocess

**States:**
```
UNENROLLED → ENROLLING → LOCKED → AUTHENTICATING → AUTHENTICATED → LOCKED
```

**Session rules:**
- Session opens on successful PPG match
- Session closes after 30 consecutive seconds without PPG contact
- Failed authentication: retry for 10 seconds, then enter 60-second cooldown
- Max 5 failed attempts per 10 minutes before requiring manual reset

### Haptic Service

**Responsibilities:** Pattern playback queue → DRV2605L control → priority management

**Stack:**
- DRV2605L driver: custom Python via `smbus2`
- Pattern library: JSON-defined waveform descriptors
- Priority queue: `queue.PriorityQueue`
- ZeroMQ subscriber: listens for pattern trigger events

**Pattern trigger message format:**
```json
{
  "pattern": "social.family",
  "priority": 2,
  "repeat": 1,
  "delay_ms": 0
}
```

### Thermal Service (Peltier)

**Responsibilities:** Warmth notification delivery → thermal safety enforcement

**Stack:**
- GPIO PWM via `RPi.GPIO` or `pigpio`
- Safety: maximum 30-second activation, 60-second cooldown, temperature monitoring via thermistor

**Thermal safety limits:**
- Maximum surface temperature delta: +8°C above ambient
- Activation abort if thermistor reads > 45°C surface temp
- Cooldown enforcement via service-level state machine

### Light Service

**Responsibilities:** Ambient LED ring control → COB LED control → notification color language

**Stack:**
- SK6812 RGBW control via `rpi-ws281x`
- COB LED via PWM + constant-current driver

**Notification color language:**
| Color | Meaning |
|-------|---------|
| Amber (warm) | Family contact |
| Blue | System / informational |
| Green | Confirmation / navigation |
| White | Torch / illumination mode |
| Red | Urgent / emergency |
| Purple | AI / Minion activity |

### Minion Context Service

**Responsibilities:** Memory read/write → context assembly for voice pipeline → sync with Minion cloud

**Stack:**
- Local SQLite database for on-device memory
- `httpx` async client for Minion cloud sync
- Context window assembly: retrieves top-K relevant memories based on current voice query

**Data model:**
```python
@dataclass
class Memory:
    id: str
    content: str
    type: str  # "conversation", "fact", "reminder", "health", "contact"
    timestamp: datetime
    relevance_tags: list[str]
    embedding: list[float]  # for semantic retrieval
```

### Cellular / Connectivity Manager

**Responsibilities:** LTE modem management → call routing → SMS → connection state monitoring

**Stack:**
- Quectel EC25 via `pyserial` (AT command interface)
- SIP stack: `pjsua2` (PJSIP Python bindings)
- SMS: AT+CMGS via modem serial interface

---

## Startup Sequence

```
1. Power on → CM4 boot (Raspberry Pi OS, ~15 seconds)
2. systemd starts all services in dependency order:
   a. identity-service (must enroll or authenticate before others fully activate)
   b. cellular-manager
   c. haptic-service
   d. thermal-service
   e. light-service
   f. minion-context-service
   g. voice-pipeline (last — depends on all others)
3. If unenrolled: boot into enrollment mode (voice-guided)
4. If enrolled: PPG authentication attempt
5. Authenticated: startup haptic pattern + amber ring pulse
6. Voice pipeline activates, waiting for wake word
```

---

## Offline Capability

The following functions operate without network:
- Calls (LTE cellular, no internet required)
- SMS
- Wake word detection
- PPG authentication
- Haptic patterns
- Thermal notifications
- LED control
- Navigation (cached OSM tiles, last 50km radius)
- Voice interaction (local LLM, limited capability)

The following require network:
- Full LLM capability (Claude API)
- Minion cloud sync
- High-quality TTS
- Real-time traffic for navigation

---

## Development Notes

**Prototype firmware is not production firmware.** The CM4 implementation is a validation platform. Production firmware will require:
- RTOS or hardened Linux (Yocto)
- Formal power state management (S1/S2/S3 equivalents)
- OTA update system with rollback
- Secure boot chain
- Hardware security module integration (not TPM)

These are post-prototype concerns. The current goal is validating the interaction paradigm, not shipping production code.

---

*Firmware spec current as of April 2026.*
