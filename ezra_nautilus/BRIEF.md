# Ezra — Nautilus Shell Form Factor

**Cursor / Blender Agent Specification v2.0 · April 2026 · Primary design direction**

Full prose (“the stone is calm…”) lives in product docs; this file + `scripts/build_ezra_nautilus.py` capture **geometry, ribs, materials, features, and outputs**.

---

## 1 — Shape (one line)

Smooth white mineral stone like the **exterior of a nautilus**: **half-moon crescent** silhouette, pocket-thin, **8 longitudinal ribs** on the convex face with **parabolic valleys** (light chambers). Ambidextrous (LR symmetric).

---

## 2 — Form factor

| Quantity | Value |
|----------|--------|
| Silhouette bbox | **93 mm** wide × **80 mm** tall (origin at geometric center) |
| Thickness (smooth taper) | **28 mm** outer arc (top) · **22 mm** mid · **14 mm** curl (bottom) |
| Convex crown | up to **~8 mm** added height (center falloff) |
| Concave resting face | up to **~4 mm** bowl (center) |
| Ribs | **8**, spiral-twisted radial from curl · crest **3.5 mm** (outer) → **1.5 mm** (curl) · crest width **~4 mm** effective |

**Held:** wide arc **top**, curl **bottom / heel**. **Desk:** rests on **concave** face; convex ribbed face **up**.

---

## 3 — Ribs & light (design intent)

- **8 raised ribs**, valleys = **7 chambers** × **2 faces** (material zones in procedural pass).
- Rib crest: polished response (lower roughness); valley: matte + emission when “active”.
- **Fibonacci idle timing** (89, 144, 233… ms): implement in sequencer / drivers later — not in static mesh script.

---

## 4 — Material (Blender targets)

- Base **RGB(248, 245, 240)**, SSS **0.38**, radius **(1.2, 1.0, 0.8)**.
- Roughness mix: valley **0.65**, crest **0.15**; specular valley **0.08**, crest **0.35**, **IOR 1.48**.
- Veining: Voronoi/Musgrave analogue — sparse grey **RGB(200, 194, 185)**, mix **~0.28**.
- Emission: valleys + curl; strengths **passive 0 / active 1.4 / curl peak 2.2** (tunable).

---

## 5 — Features (both convex faces in symmetric build)

| Feature | Placement (approx, mm, origin center) |
|---------|----------------------------------------|
| Sensor recess | **φ point**: **(0, −10)** plane (30 mm “up” from curl toward top), **⌀14 mm**, depth **2 mm**, **both** convex sides |
| USB-C | Curl bottom center **(0, −40)**, **9 × 3.5 mm** |
| Laser | Curl tip **(0, −40)** region, **⌀3 mm** |
| Speakers | **L/R** edges, upper third — simplified **20 × 12 mm** slots |

Spec calls for hole grille arrays — script uses **slots**; replace with boolean hole pattern in Blender.

---

## 6 — Renders & deliverables

Filenames: `hero_convex`, `hero_curl`, `profile_side`, `desk_resting`, `in_hand_right`, `in_hand_left`, `fibonacci_sequence`, `macro_rib`, `macro_sensor`, turntable **72** @ **25°** elevation.

Deliverable tree:

```
ezra_nautilus/
├── ezra_nautilus.blend
├── ezra_material.blend   (optional link lib)
├── renders/
├── turntable/
├── exports/              (.obj / .glb / .stl)
└── scripts/build_ezra_nautilus.py
```

---

## 7 — Implementation notes

Procedural mesh is an **approximation**: silhouette polygon → grid fill → **variable thickness + convex/concave + 8 spiral-phase radial ribs** + booleans. Replace silhouette **NURBS** and **true filleted rib sweeps** in a manual CAD polish pass (spec Step 1–7).

Older rectangular/spiral experiments were removed; **nautilus is the single shell track** in this repo.

**Cursor ↔ Blender MCP:** install `ezra_nautilus/blender_mcp/addon.py` in Blender (Preferences → Add-ons), start server on **9876**, match `~/.cursor/mcp.json` `blender` entry.
