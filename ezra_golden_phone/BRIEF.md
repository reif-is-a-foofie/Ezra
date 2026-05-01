# Ezra — Skip Stone Form Factor

Primary industrial-design direction for the screenless personal device form.

## Geometry

| Quantity | Value |
|----------|-------|
| Face envelope | 116 mm × 64 mm |
| Ratio | 1.8125; φ-influenced elongated skip-stone proportion |
| Thickness | 15 mm center / hard-tapered 5.5 mm visual edge |
| Plan geometry | Not a perfect oval: faster narrower leading end, broader calmer trailing end |
| Edge softening | Strong lens-profile taper; edges feel remarkably thin |
| Weight target | 165 g |
| Material | Warm white Corian/KRION mineral composite |

The object should read as a refined skipping stone: ancient and advanced, calm and capable. The center carries battery/compute mass while the perimeter visually disappears.

Create tactile asymmetry hidden inside visual calm. Orientation should be obvious in hand but subtle to the eye: upper-right thumb shelf, left finger sweep, lower-center palm swell, and a softly diagonalized long axis.

## Sacred Geometry Rules

| Rule | Value |
|------|-------|
| Governing short axis | 64 mm adult palm datum |
| Long axis | 116 mm |
| φ ratio note | A/B = 1.8125; intentionally beyond pure φ for pocket/hand utility |
| Superellipse exponent | n = 2.5 |
| Crown peak | 71.7 mm from trailing end, 13.7 mm ahead of true center |
| Feet | Golden gnomon triangle: `(43,0)`, `(-20,-20)`, `(-20,+20)` mm |
| Foot triangle | 40 mm base, 66.1 mm legs, apex angle 35.2° ≈ 36° |
| Fibonacci spiral | Construction guide only: the flattened nautilus logic derives the shape; it is not a lit or engraved feature |

## Functional Zones

| Zone | Placement |
|------|-----------|
| Qi2/MagSafe-style charging | Hidden centered rear packaging envelope, not an exterior design feature |
| Sapphire PPG eye | Lower front/palm face, 12 mm disc |
| Thermal presence zone | Lower rear face, 40 mm square packaging envelope |
| Speaker | Upper face/edge, slot or hidden acoustic mesh |
| Microphones | Four-point golden-rectangle perimeter grid |
| Ambient glow | 0.6 mm perimeter seam light channel, not a screen |
| Flood light | Bottom face: wide flood band / focused flashlight band / wide flood band |
| UV-A | Two underside inspection emitters near trailing underside edge |
| Feet | Three silicone-capped Corian feet hold the bottom light surface off table |
| USB-C | Bottom short edge |

## Material/Light Intent

Corian/KRION remains the dominant surface: matte, dense, mineral, warm white with fine organic gray flecks. The internal glow should emerge through the stone and perimeter seam, never as exposed LEDs, a display, notification badge, attention rectangle, or visible charging ring.

Run:

```sh
blender --background --python ezra_golden_phone/scripts/build_ezra_golden_phone.py -- --save-blend --export-all --render-hero
```

Use `--show-features` for exterior feature placement reviews and `--show-packaging` for engineering reviews; the default build is pure exterior form plus hidden glow.

Prototype BOM and Onshape packaging notes:
[`PROTOTYPE_BUILD_PLAN.md`](./PROTOTYPE_BUILD_PLAN.md)
