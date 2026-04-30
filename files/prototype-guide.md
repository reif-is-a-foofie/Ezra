# Ezra — Investor Prototype Build Guide

**Goal:** Produce a credible sensory demonstration of the Ezra experience in 2–3 weeks for under $3,000, without manufacturing a production-ready device.

The investor prototype is not proof of manufacturing. It is proof of experience. The question investors need answered is: *does this interaction paradigm work?* Can I hold something, speak to it, feel it respond, and understand why someone would choose this over a phone? That question can be answered with a well-built prototype shell and a phone tethered in your pocket.

---

## Layer 1 — Physical Shell

**Goal:** An object investors can hold. Weight, texture, and material are the first sensory argument.

**Parts needed:**
- 1× KRION or Corian billet, approximately 130×75×35mm
- Access to a CNC shop (local fabricators, Xometry, Protolabs)
- Sandpaper: 220, 400, 800, 1200 grit
- Matte clear coat (optional)

**Process:**

1. Source KRION from a Porcelanosa distributor or Corian from a kitchen countertop fabricator. Small off-cut pieces are often available cheaply or free.

2. Provide the CNC shop with a basic 3D model (STEP file) defining:
   - The exterior river-stone profile (rounded corners, bilateral grip indent on each long face)
   - A hollow interior cavity (wall thickness ~6mm)
   - The 12mm circular sensor window recess on the lower face
   - A flat bottom face for the Peltier contact zone

3. After CNC milling, hand-sand exterior surfaces through grits to 1200. The finish should feel like a polished stone — not glossy, not rough. Matte is correct.

4. The shell does not need internals for the first investor meeting. The object in their hand is the argument. Approximate the correct weight with internal ballast (lead sheet, steel shot in epoxy) if needed.

**Cost:** $500–1,500 for CNC; $40–80 for material.  
**Time:** 1–2 weeks (including fabricator lead time).

---

## Layer 2 — Voice and Memory Demo

**Goal:** Demonstrate the voice interaction paradigm with plausible memory and context.

**Architecture:**

```
iPhone/Android (in pocket) → Bluetooth → Speaker in shell → User voice → Whisper API → Claude API → TTS → Speaker
```

This is a tethered demo. The phone does the compute. The shell contains only a speaker and a Bluetooth receiver (e.g., Adafruit Feather Bluefruit or similar). The user does not see the phone.

**Pre-load five demo scripts** into the Claude system prompt as memory context:

```
User's name: [name]
Recent meals: Nobu on Thursday (expense account), home-cooked salmon Friday
Recent stress events: Investor meeting prep, contract review with attorney
Upcoming: Flight to Austin on May 12, meeting with LP at 2pm
Contacts: Mom (Margaret), work partner (Alex)
```

Then demo these five interactions:

1. "Ezra, where did we eat last Thursday?"  
   → "You had dinner at Nobu on Thursday."

2. "What's my stress level been looking like?"  
   → "Your heart rate variability has been lower than your baseline for the past three days. The pattern usually correlates with high-pressure preparation periods. Do you want me to block your morning for a walk?"

3. "Remind me about the Austin flight."  
   → "You fly to Austin on May 12th. Your LP meeting is at 2pm. Should I set a departure reminder?"

4. "Is there anything from Mom?"  
   → "Margaret called at 9:47am. She didn't leave a message."

5. "Ezra, I need to think. Hold calls for an hour."  
   → "Done. I'll hold everything except Margaret and emergency contacts until 3:15."

**Cost:** Bluetooth receiver + speaker: $50–100. API costs: negligible.  
**Time:** 3–5 days for assembly and prompt engineering.

---

## Layer 3 — Haptic Demonstration

**Goal:** Show that the device communicates through touch in a meaningfully different way than a phone vibration.

**Parts:**
- 1× Lofelt L5 LRA (or Adafruit DRV2605L breakout + LRA motor)
- 1× Raspberry Pi Zero 2W or Arduino
- 1× small LiPo battery
- Jumper wire, foam tape

**Wire:** Pi Zero → DRV2605L driver (I2C) → LRA. Mount the LRA to the interior shell wall with foam tape on three sides (isolation prevents rattle).

**Program three patterns** to demonstrate via button trigger during the demo:

```python
# Pattern 1: Ambient notification (slow, soft)
AMBIENT = [(150, 0.3), (0, 0.2), (150, 0.3)]  # Hz, duration

# Pattern 2: Incoming call (double pulse, firmer)
CALL = [(200, 0.1), (0, 0.1), (200, 0.1), (0, 0.5)]

# Pattern 3: "Loved one" pattern (warm slow throb)
MOM = [(80, 0.8), (0, 0.4), (80, 0.8)]
```

Demo script: "Feel this — this is a standard notification. Now feel this — this is your mom. Notice the difference? The device is already communicating meaning before you consciously process it."

**Cost:** ~$100–150 for components.  
**Time:** 3–5 days for assembly and programming.

---

## Layer 4 — Warmth Demonstration (Optional but High-Impact)

**Parts:**
- 1× Peltier TEC1-12706
- 1× copper heat spreader plate
- 1× Pi Zero 2W PWM GPIO → MOSFET → TEC
- 1× 5V 4A power supply (demo rig only)

**Wire:** Pi Zero GPIO → MOSFET gate → TEC+ (TEC− to power GND, copper plate on hot side).

**Demo:** Hand the shell to the investor. Trigger the warmth sequence from your phone via Bluetooth. The shell surface temperature rises 4–6°C in about 3 seconds. Say: "That's a message from your mom. You felt it before I told you what it was."

This is the most memorable 10 seconds in the demo. It activates a sensory channel no other consumer device uses for communication.

**Cost:** ~$30–50 for components.  
**Time:** 2–3 days.

---

## Full Demo Script (15 minutes)

1. **Hand them the shell (60 seconds).** Say nothing. Let them hold it. Let them notice the weight, the texture, the material. Most people will ask what it is.

2. **"It doesn't have a screen." (30 seconds).** Let that land. Answer the obvious question: "Yes, it makes calls. Yes, it knows your calendar. It does everything your phone does except show you a feed."

3. **Voice demo (5 minutes).** Run through the five interactions. Emphasize the memory: "It knows you."

4. **Haptic demo (2 minutes).** Pass it to them, run the patterns. Ask them to feel the difference between ambient, call, and loved one.

5. **Warmth (1 minute).** Trigger the Peltier. Let them experience it.

6. **The ask (remainder).** You have demonstrated that the experience paradigm is real, believable, and emotionally distinct from any existing product.

---

## What This Prototype Does Not Demonstrate

- Full PPG authentication (this requires the sapphire window, MAX30102, and security element integration — target for prototype v2)
- Cellular calling (tethered to phone; present as "demo mode")
- Production audio quality (directional microphone array)
- Battery life

These gaps are appropriate. Investors are funding the concept and the team, not the finished hardware. The prototype answers the question they need answered: *is this real?*

---

*Build guide current as of April 2026.*
