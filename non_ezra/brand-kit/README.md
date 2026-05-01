# Good Industries — Brand Kit

The complete kit for **Good Industries** (the venture studio) and **The Studio** (its flagship innovation center).

> *Build the change you wish to see in the world.*

---

## What's here

| File / folder | Purpose |
|---|---|
| `01_brand_strategy.docx` | Positioning, audiences, voice, naming hierarchy, design principles |
| `02_visual_identity_guidelines.docx` | Logo usage, color, type, do/don'ts, application examples |
| `logos/` | Source SVGs for all marks and lockups |
| `logos/png/` | Rendered PNGs at 1×, 2×, 4× — **transparent backgrounds**, drag-and-drop ready |
| `signage/` | Source SVGs for warehouse banner, wall sign, bay sign, workbench label, exterior sign, coverall patch |
| `signage/png/` | Rendered PNGs at 1×, 2×, 4× |

---

## Naming hierarchy

**The Good Project** → mission · **Good Industries** → operating venture studio · **The Studio** → physical innovation center · **Ezra** → first product

On any external surface, the chain must be visible at least once: *Product · Good Industries · The Good Project.*

---

## Logos — quick picker

For a slide / page on a **dark** background, use:
- `logos/png/g-mark-light@2x.png` — primary mark
- `logos/png/good-industries-horizontal-onDark@2x.png` — wordmark
- `logos/png/the-studio-onDark@2x.png` — Studio wordmark
- `logos/png/ezra-onDark@2x.png` — Ezra product lockup
- `logos/png/motto-onDark@2x.png` — motto block

For a slide / page on a **light** background, use:
- `logos/png/g-mark-dark@2x.png` — primary mark
- `logos/png/good-industries-horizontal-light@2x.png` — wordmark
- `logos/png/the-studio-light@2x.png` — Studio wordmark
- `logos/png/ezra-onLight@2x.png` — Ezra product lockup
- `logos/png/motto-onLight@2x.png` — motto block

For accent / hero moments on dark, use:
- `logos/png/g-mark-brass@2x.png` — brass mark

For etching, embossing, branding irons, embroidery:
- `logos/png/g-mark-outline@2x.png` — outline only

---

## Color tokens

| Name | Hex | Use |
|---|---|---|
| Ink | `#0E0F12` | Primary surface; reversed type background |
| Graphite | `#1A1C20` | Banner backgrounds; product photography |
| Concrete | `#3A3D43` | Mid grey; rules; secondary surfaces |
| Steel | `#6B6E74` | Captions; metadata |
| Bone | `#F1ECE3` | Reversed type; light surface; primary text on dark |
| Paper | `#FAF7F1` | Lightest neutral; printed page background |
| Brass | `#B08A4A` | Primary accent; subtitles; rules |
| Copper | `#8C5A2F` | Deeper accent for light surfaces |
| Forge | `#D9622B` | Signal only — alarms, fire, urgency |

Target ratio per surface: **70% Ink · 25% Bone/Paper · 5% Brass.** Forge is signal-only.

---

## Type stack

- **Display / Headings / Body:** Inter (free, rsms.me/inter). Fallback: Helvetica Neue → Arial → Liberation Sans.
- **Mono / Technical:** IBM Plex Mono. For specs, station IDs, version numbers.
- **Serif (rare):** Source Serif 4. Reserved for scriptural epigraphs and the most considered prose.

Set tight. Use weight to create hierarchy. Display sizes use −0.04em tracking.

---

## File naming

PNG variants are tagged with scale: `@1x` (native), `@2x` (decks, web hi-DPI), `@4x` (large print, billboards).

Lockups tagged `onDark` / `onLight` have transparent backgrounds and are color-tuned for that surface family.

Lockups tagged `dark` / `light` (without "on") include a colored rectangle background — use only when you need an opaque tile.

---

## Source of truth

SVG is the source of truth. PNGs are derived. If you need a custom size or a new variant, edit the SVG and re-render — do not modify PNGs in place.

To re-render PNGs after editing SVGs, run the rasterizer (Python, requires `cairosvg`):
```
python3 rasterize.py
```
