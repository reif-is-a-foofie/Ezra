# Ezra — Haptic Language Specification

## Philosophy

A haptic vocabulary works only if it is learnable. The goal is not to encode as much information as possible into vibration — it is to encode a small number of meanings so distinctly that the user internalizes them without conscious study.

Ezra's haptic language draws from two design principles:

1. **Rhythm communicates urgency.** Slow patterns are ambient; fast patterns are urgent. This mirrors natural alarm systems (a heartbeat vs. a car horn).
2. **Texture communicates identity.** The specific waveform shape — not just the rhythm — can encode whether a notification comes from family, from work, or from the system.

---

## Hardware Capability

The Lofelt L5 LRA (linear resonant actuator) can play arbitrary waveforms in the 50–300Hz range. At low frequencies (50–80Hz), the sensation reads as warm and diffuse — similar to the purr of a cat. At higher frequencies (180–300Hz), it reads as sharp and crisp. This frequency dimension gives Ezra a second axis of communication beyond rhythm.

The DRV2605L driver supports both ROM waveforms and custom waveform RAM. Ezra uses custom waveforms to allow fine-grained pattern design.

---

## Pattern Library

### Tier 0 — Ambient (Non-interruptive)

These patterns are designed to be perceptible but not demanding. The user can ignore them without missing anything critical.

| Pattern | Waveform | Meaning |
|---------|----------|---------|
| `ambient.heartbeat` | 80Hz, 0.6s on, 0.4s off, 0.3s on | General notification — read at your convenience |
| `ambient.pulse` | 60Hz, 1.2s slow ramp up then ramp down | System status — everything is fine |

### Tier 1 — Informational (Mild interrupt)

| Pattern | Waveform | Meaning |
|---------|----------|---------|
| `info.message` | 120Hz, 0.15s on, 0.1s off, 0.15s on | New message received |
| `info.reminder` | 150Hz, 0.1s × 3 with 0.08s gaps | Reminder fired |
| `info.navigation` | 200Hz, 0.2s on | Waypoint approaching |
| `info.navigation_turn` | 200Hz, 0.1s on × 3 rapid | Turn now |

### Tier 2 — Social (Identity-encoded)

These patterns are distinct enough that the user learns to associate them with specific contact types.

| Pattern | Waveform | Meaning |
|---------|----------|---------|
| `social.family` | 70Hz, 0.8s slow throb | Message or call from designated family contact |
| `social.call_incoming` | 180Hz, 0.2s on, 0.2s off × repeating | Incoming call (generic) |
| `social.call_family` | 70Hz, 0.5s throb, 0.2s gap × repeating | Incoming call from family contact |
| `social.call_missed` | 150Hz, 0.1s on, 0.05s off × 2, 0.4s gap | Missed call notification |

### Tier 3 — Urgent (Full interrupt)

| Pattern | Waveform | Meaning |
|---------|----------|---------|
| `urgent.alert` | 250Hz, 0.1s × 3 sharp | Urgent notification |
| `urgent.emergency` | 300Hz, continuous for 2s | Emergency alert |
| `urgent.sos` | 250Hz, 3× short + 3× long + 3× short | SOS / crisis |

### Tier 4 — Feedback (Confirmation and error)

| Pattern | Waveform | Meaning |
|---------|----------|---------|
| `feedback.confirm` | 150Hz, 0.05s, then 200Hz, 0.1s (rising double) | Action confirmed |
| `feedback.deny` | 200Hz, 0.2s on, 0.05s off, 0.2s on (flat double) | Action denied / error |
| `feedback.end` | 80Hz, 0.5s tapering off | Session ending / call ending |

---

## Warmth Integration

Warmth from the Peltier element is always paired with a haptic pattern for the `social.family` context. The combination is:

```
social.family haptic pattern → 1 second → Peltier warmth ramp (3 seconds to +5°C delta)
```

The haptic gets the user's attention; the warmth is the message. This pairing ensures the warmth is not missed (the user may have set the device down) while giving warmth its full expressive weight.

---

## Learning Curve

User testing (anticipated) will validate whether naive users can learn to distinguish patterns within:
- Day 1: Urgent vs. non-urgent (rhythm discriminability)
- Week 1: Family vs. generic (frequency/texture discriminability)
- Week 4: Full pattern vocabulary (12–15 patterns)

The hypothesis is that the most important discriminations are learnable in the first 24 hours of use, and the full vocabulary is internalized within a month — comparable to learning to read a watch.

---

## Implementation Notes

Pattern triggers originate from the voice AI stack and are dispatched via a ZeroMQ message queue to the haptic service running as a daemon. This allows the voice pipeline and the haptic system to operate independently.

```python
# Example: trigger social.family pattern
import zmq
context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.connect("tcp://localhost:5555")
socket.send_json({"pattern": "social.family", "priority": 2})
```

Pattern priority (1–5) determines behavior when patterns queue:
- Priority 1 (ambient): drop if queue is not empty
- Priority 3 (social): play after current pattern completes
- Priority 5 (urgent): interrupt current pattern immediately

---

*Haptic language spec v0.2 — subject to revision based on user testing.*
