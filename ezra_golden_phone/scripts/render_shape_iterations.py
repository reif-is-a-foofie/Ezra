#!/usr/bin/env python3
"""Render plain shape studies before material/mesh/detail decisions."""

from __future__ import annotations

import argparse
import importlib.util
import math
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
BASE_SCRIPT = SCRIPT_DIR / "build_ezra_golden_phone.py"
OUT_DIR = ROOT / "shape_iterations"


def load_builder():
    spec = importlib.util.spec_from_file_location("ezra_builder", BASE_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load Ezra builder script")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VARIANTS = [
    {
        "slug": "A_reference_oval",
        "title": "A - Reference Oval",
        "notes": "Closest to the hand stone: simple oval, felt asymmetry, least gadget-like.",
        "LENGTH_MM": 108.0,
        "WIDTH_MM": 65.0,
        "HEAD_WIDTH_MM": 61.5,
        "CENTER_THICKNESS_MM": 19.5,
        "EDGE_THICKNESS_MM": 7.2,
        "SUPERELLIPSE_N": 2.28,
        "CROWN_MM": 3.2,
        "CROWN_OFFSET_X_MM": -6.0,
        "THUMB_FLATTEN_SCALE": 0.955,
    },
    {
        "slug": "B_golden_pebble",
        "title": "B - Golden Pebble",
        "notes": "Current spec translated into a more natural pebble, still phone/pocket scaled.",
        "LENGTH_MM": 108.0,
        "WIDTH_MM": 66.0,
        "HEAD_WIDTH_MM": 63.0,
        "CENTER_THICKNESS_MM": 21.0,
        "EDGE_THICKNESS_MM": 8.0,
        "SUPERELLIPSE_N": 2.65,
        "CROWN_MM": 2.8,
        "CROWN_OFFSET_X_MM": -5.0,
        "THUMB_FLATTEN_SCALE": 0.962,
    },
    {
        "slug": "C_thinner_pocket",
        "title": "C - Thinner Pocket",
        "notes": "More pocketable and less object-heavy; may lose heirloom density.",
        "LENGTH_MM": 108.0,
        "WIDTH_MM": 64.0,
        "HEAD_WIDTH_MM": 61.0,
        "CENTER_THICKNESS_MM": 17.5,
        "EDGE_THICKNESS_MM": 6.5,
        "SUPERELLIPSE_N": 2.5,
        "CROWN_MM": 2.4,
        "CROWN_OFFSET_X_MM": -5.5,
        "THUMB_FLATTEN_SCALE": 0.958,
    },
    {
        "slug": "D_fuller_heirloom",
        "title": "D - Fuller Heirloom",
        "notes": "Most stone-like mass and warmth; strongest hand presence.",
        "LENGTH_MM": 106.0,
        "WIDTH_MM": 67.0,
        "HEAD_WIDTH_MM": 62.5,
        "CENTER_THICKNESS_MM": 22.0,
        "EDGE_THICKNESS_MM": 8.8,
        "SUPERELLIPSE_N": 2.22,
        "CROWN_MM": 3.6,
        "CROWN_OFFSET_X_MM": -7.0,
        "THUMB_FLATTEN_SCALE": 0.952,
    },
    {
        "slug": "E_thumb_index",
        "title": "E - Thumb Index",
        "notes": "Same visual calm, stronger one-side flattening for pocket orientation.",
        "LENGTH_MM": 108.0,
        "WIDTH_MM": 66.0,
        "HEAD_WIDTH_MM": 62.0,
        "CENTER_THICKNESS_MM": 20.0,
        "EDGE_THICKNESS_MM": 7.5,
        "SUPERELLIPSE_N": 2.42,
        "CROWN_MM": 3.0,
        "CROWN_OFFSET_X_MM": -6.0,
        "THUMB_FLATTEN_SCALE": 0.935,
    },
    {
        "slug": "F_soft_capsule",
        "title": "F - Soft Capsule",
        "notes": "More phone-compatible silhouette; safer for chargers but less natural.",
        "LENGTH_MM": 112.0,
        "WIDTH_MM": 66.0,
        "HEAD_WIDTH_MM": 64.0,
        "CENTER_THICKNESS_MM": 19.0,
        "EDGE_THICKNESS_MM": 7.0,
        "SUPERELLIPSE_N": 3.0,
        "CROWN_MM": 2.5,
        "CROWN_OFFSET_X_MM": -4.0,
        "THUMB_FLATTEN_SCALE": 0.965,
    },
    {
        "slug": "G_flat_hand_pebble",
        "title": "G - Flat Hand Pebble",
        "notes": "Closest to the grey reference: broad horizontal palm stone, low dome, soft lens edge.",
        "LENGTH_MM": 108.0,
        "WIDTH_MM": 69.0,
        "HEAD_WIDTH_MM": 66.0,
        "CENTER_THICKNESS_MM": 15.0,
        "EDGE_THICKNESS_MM": 5.5,
        "SUPERELLIPSE_N": 2.18,
        "STONE_SIDE_EXPONENT": 0.34,
        "CROWN_MM": 1.8,
        "CROWN_OFFSET_X_MM": -5.0,
        "THUMB_FLATTEN_SCALE": 0.955,
    },
    {
        "slug": "H_skipping_stone",
        "title": "H - Skipping Stone",
        "notes": "Thinnest and calmest; very pocketable, but internal packaging becomes harder.",
        "LENGTH_MM": 110.0,
        "WIDTH_MM": 68.0,
        "HEAD_WIDTH_MM": 65.5,
        "CENTER_THICKNESS_MM": 13.5,
        "EDGE_THICKNESS_MM": 4.8,
        "SUPERELLIPSE_N": 2.05,
        "STONE_SIDE_EXPONENT": 0.30,
        "CROWN_MM": 1.4,
        "CROWN_OFFSET_X_MM": -4.0,
        "THUMB_FLATTEN_SCALE": 0.960,
    },
    {
        "slug": "I_weighted_river_stone",
        "title": "I - Weighted River Stone",
        "notes": "Reference-like broad face with more belly for battery and hand warmth.",
        "LENGTH_MM": 106.0,
        "WIDTH_MM": 70.0,
        "HEAD_WIDTH_MM": 66.0,
        "CENTER_THICKNESS_MM": 17.0,
        "EDGE_THICKNESS_MM": 6.2,
        "SUPERELLIPSE_N": 2.12,
        "STONE_SIDE_EXPONENT": 0.38,
        "CROWN_MM": 2.2,
        "CROWN_OFFSET_X_MM": -6.5,
        "THUMB_FLATTEN_SCALE": 0.948,
    },
    {
        "slug": "J_skip_stone_spec",
        "title": "J - Skip Stone Spec",
        "notes": "Direct translation of the new brief: 103 x 75 x 17.5 mm, broad and thin with lens taper.",
        "LENGTH_MM": 103.0,
        "WIDTH_MM": 75.0,
        "HEAD_WIDTH_MM": 71.0,
        "CENTER_THICKNESS_MM": 17.5,
        "EDGE_THICKNESS_MM": 6.5,
        "SUPERELLIPSE_N": 2.08,
        "STONE_SIDE_EXPONENT": 0.31,
        "CROWN_MM": 1.0,
        "CROWN_OFFSET_X_MM": -5.5,
        "THUMB_FLATTEN_SCALE": 0.952,
        "THUMB_CONCAVITY_MM": 2.0,
        "DIAGONAL_SKEW_MM": 1.4,
        "TAIL_BROADEN_MM": 2.4,
    },
    {
        "slug": "K_athletic_skip_stone",
        "title": "K - Athletic Skip Stone",
        "notes": "Faster leading end and stronger diagonal energy; more capable/tool-like.",
        "LENGTH_MM": 104.0,
        "WIDTH_MM": 74.0,
        "HEAD_WIDTH_MM": 68.5,
        "CENTER_THICKNESS_MM": 16.8,
        "EDGE_THICKNESS_MM": 6.0,
        "SUPERELLIPSE_N": 2.02,
        "STONE_SIDE_EXPONENT": 0.29,
        "CROWN_MM": 0.8,
        "CROWN_OFFSET_X_MM": -5.0,
        "THUMB_FLATTEN_SCALE": 0.948,
        "THUMB_CONCAVITY_MM": 2.8,
        "DIAGONAL_SKEW_MM": 2.2,
        "TAIL_BROADEN_MM": 3.2,
    },
    {
        "slug": "L_heavy_skip_stone",
        "title": "L - Heavy Skip Stone",
        "notes": "Keeps the skip-stone plan but restores internal volume for battery/speakers.",
        "LENGTH_MM": 103.0,
        "WIDTH_MM": 75.0,
        "HEAD_WIDTH_MM": 70.0,
        "CENTER_THICKNESS_MM": 18.5,
        "EDGE_THICKNESS_MM": 6.5,
        "SUPERELLIPSE_N": 2.18,
        "STONE_SIDE_EXPONENT": 0.34,
        "CROWN_MM": 1.3,
        "CROWN_OFFSET_X_MM": -6.5,
        "THUMB_FLATTEN_SCALE": 0.950,
        "THUMB_CONCAVITY_MM": 2.1,
        "DIAGONAL_SKEW_MM": 1.2,
        "TAIL_BROADEN_MM": 2.8,
    },
]


def apply_variant(builder, variant):
    for key, value in variant.items():
        if key.isupper():
            setattr(builder, key, value)


def render_variant(builder, variant):
    import bpy

    apply_variant(builder, variant)
    builder.build_scene(passive=True, show_features=False, show_packaging=False, show_mesh=False, clay=True)
    bpy.context.scene.render.engine = "CYCLES"
    bpy.context.scene.cycles.samples = 16
    bpy.context.scene.render.resolution_x = 900
    bpy.context.scene.render.resolution_y = 650
    bpy.context.scene.view_settings.exposure = -1.35
    bpy.context.scene.camera.location = (0.118, -0.175, 0.088)
    bpy.context.scene.camera.rotation_euler = (math.radians(63), 0, math.radians(36))
    bpy.context.scene.camera.data.lens = 62
    bpy.context.scene.render.filepath = str(OUT_DIR / f"{variant['slug']}.png")
    bpy.ops.render.render(write_still=True)


def write_board():
    lines = [
        "# Ezra Shape Iterations",
        "",
        "Shape-only review. No mesh, no glow, no sensors, no material detailing.",
        "",
        "| Variant | Render | Notes |",
        "|---------|--------|-------|",
    ]
    for variant in VARIANTS:
        lines.append(f"| {variant['title']} | ![]({variant['slug']}.png) | {variant['notes']} |")
    lines.append("")
    lines.append("Recommendation: choose silhouette first, then apply Corian/KRION material, luminous mesh, PPG island, charger packaging, and scene lighting to one selected direction.")
    (OUT_DIR / "README.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", nargs="*", help="Variant slug prefixes to render, e.g. J K L")
    script_args = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    args = parser.parse_args(script_args)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    builder = load_builder()
    selected = VARIANTS
    if args.only:
        prefixes = tuple(args.only)
        selected = [variant for variant in VARIANTS if variant["slug"].startswith(prefixes)]
    for variant in selected:
        render_variant(builder, variant)
    write_board()


if __name__ == "__main__":
    main()
