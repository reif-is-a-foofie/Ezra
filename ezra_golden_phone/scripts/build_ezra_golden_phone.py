#!/usr/bin/env python3
"""
Build Ezra's skip-stone companion-device concept.

Outputs a thin, warm-white translucent mineral body with amber internal glow.
Packaging guides are opt-in so hidden internals do not pollute the exterior read.
"""

from __future__ import annotations

import argparse
import math
import random
import sys
from pathlib import Path

MM = 0.001

PHI = 1.6180339887
PALM_AXIS_MM = 64.0
LENGTH_MM = 116.0
WIDTH_MM = PALM_AXIS_MM
HEAD_WIDTH_MM = 60.0
CENTER_THICKNESS_MM = 15.0
EDGE_THICKNESS_MM = 5.5
CROWN_OFFSET_X_MM = LENGTH_MM / PHI - LENGTH_MM / 2.0
THUMB_FLAT_SIDE = -1.0
THUMB_FLATTEN_SCALE = 0.922
THUMB_CONCAVITY_MM = 2.0
DIAGONAL_SKEW_MM = 1.2
TAIL_BROADEN_MM = 2.2
EDGE_FILLET_MM = 7.5
CROWN_MM = 0.60
BOTTOM_DISH_MM = 1.2
SUPERELLIPSE_N = 2.5
RADIAL_RINGS = 48
PERIMETER_SEGMENTS = 256
VERTICAL_BANDS = 36
STONE_SIDE_EXPONENT = 0.48
FOOT_RADIUS_MM = 2.5
FOOT_HEIGHT_MM = 2.0
FOOT_POSITIONS_MM = (
    ("front_golden_gnomon_foot", 43.0, 0.0, 0.0),
    ("rear_left_golden_gnomon_foot", -20.0, -20.0, 12.0),
    ("rear_right_golden_gnomon_foot", -20.0, 20.0, -12.0),
)

OUT_DIR = Path("ezra_golden_phone")
EXPORT_DIR = OUT_DIR / "exports"
RENDER_DIR = OUT_DIR / "renders"


def edge_softness(x: float, y: float) -> float:
    a = LENGTH_MM / 2.0
    b = local_half_width(x)
    norm = ((abs(x) / a) ** SUPERELLIPSE_N + (abs(y) / b) ** SUPERELLIPSE_N) ** (1.0 / SUPERELLIPSE_N)
    d = max(0.0, 1.0 - norm) * min(a, b)
    return max(0.0, min(1.0, d / EDGE_FILLET_MM))


def crown(x: float, y: float) -> float:
    nx = (x - CROWN_OFFSET_X_MM) / (LENGTH_MM / 2.0)
    ny = y / (WIDTH_MM / 2.0)
    base = max(0.0, 1.0 - 0.50 * nx * nx - 0.70 * ny * ny)
    palm_bias = 0.32 * math.exp(-(((x - CROWN_OFFSET_X_MM) / 34.0) ** 2 + (y / 27.0) ** 2))
    return CROWN_MM * (base + palm_bias)


def bottom_dish(x: float, y: float) -> float:
    """Shallow underside dish for the flood-light platform and reflector volume."""
    return BOTTOM_DISH_MM * math.exp(-((x / 44.0) ** 2 + (y / 27.0) ** 2))


def z_surfaces(x: float, y: float) -> tuple[float, float]:
    s = edge_softness(x, y)
    falloff = s * s * (3.0 - 2.0 * s)
    half = CENTER_THICKNESS_MM / 2.0
    edge_drop = (1.0 - falloff) * EDGE_FILLET_MM
    min_half = EDGE_THICKNESS_MM / 2.0
    top = max(min_half, half + crown(x, y) - edge_drop)
    bottom = min(-min_half, -half - 0.32 * crown(x, y) + edge_drop * 0.62)
    return bottom, top


def local_half_width(x: float) -> float:
    """Head (+X) is subtly narrower than tail (-X)."""
    t = max(0.0, min(1.0, (x / (LENGTH_MM / 2.0) + 1.0) * 0.5))
    smooth = t * t * (3.0 - 2.0 * t)
    return (WIDTH_MM + (HEAD_WIDTH_MM - WIDTH_MM) * smooth) / 2.0


def thumb_side_adjust(y: float) -> float:
    """Flatten thumb side just enough to feel, not enough to look crooked."""
    if y * THUMB_FLAT_SIDE <= 0:
        return y
    return y * THUMB_FLATTEN_SCALE


def organic_xy_adjust(x: float, y: float, side_scale: float) -> tuple[float, float]:
    """Tactile asymmetry hidden inside visual calm."""
    x_norm = x / (LENGTH_MM / 2.0)
    y_norm = y / max(local_half_width(x), 1.0)
    tail_bias = max(0.0, -x_norm)
    thumb_side = 1.0 if y * THUMB_FLAT_SIDE > 0 else 0.0
    concavity = THUMB_CONCAVITY_MM * thumb_side * math.exp(-((x_norm - 0.10) / 0.58) ** 2) * (0.35 + 0.65 * side_scale)
    y -= THUMB_FLAT_SIDE * concavity * (0.45 + 0.55 * abs(y_norm))
    y += DIAGONAL_SKEW_MM * x_norm * (0.22 + 0.78 * side_scale)
    x -= TAIL_BROADEN_MM * tail_bias * (1.0 - abs(y_norm)) * 0.22
    return x, y


def build_body_mesh():
    a = LENGTH_MM / 2.0
    verts = []
    rows: list[list[int]] = []

    for band in range(VERTICAL_BANDS + 1):
        phi = -math.pi / 2.0 + math.pi * band / VERTICAL_BANDS
        vertical = math.sin(phi)
        side_scale = abs(math.cos(phi)) ** STONE_SIDE_EXPONENT
        z_base = (CENTER_THICKNESS_MM / 2.0) * math.copysign(abs(vertical) ** 0.92, vertical)
        row = []
        for seg in range(PERIMETER_SEGMENTS):
            theta = 2.0 * math.pi * seg / PERIMETER_SEGMENTS
            c = math.cos(theta)
            sn = math.sin(theta)
            x = side_scale * a * math.copysign(abs(c) ** (2.0 / SUPERELLIPSE_N), c)
            local_b = local_half_width(x)
            y = side_scale * local_b * math.copysign(abs(sn) ** (2.0 / SUPERELLIPSE_N), sn)
            y = thumb_side_adjust(y)
            x, y = organic_xy_adjust(x, y, side_scale)
            crown_weight = max(0.0, vertical) ** 1.8
            bottom_weight = max(0.0, -vertical) ** 2.0
            z = z_base + crown_weight * crown(x, y) * 0.55 - bottom_weight * (crown(x, y) * 0.16 + bottom_dish(x, y))
            row.append(len(verts))
            verts.append((x * MM, y * MM, z * MM))
        rows.append(row)

    faces = []
    for band in range(VERTICAL_BANDS):
        for seg in range(PERIMETER_SEGMENTS):
            nxt = (seg + 1) % PERIMETER_SEGMENTS
            faces.append((rows[band][seg], rows[band][nxt], rows[band + 1][nxt], rows[band + 1][seg]))

    return verts, faces


def make_mat(bpy, name, base, roughness=0.55, alpha=1.0, emission=None, strength=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*base, alpha)
        bsdf.inputs["Roughness"].default_value = roughness
        if "Alpha" in bsdf.inputs:
            bsdf.inputs["Alpha"].default_value = alpha
        if "Metallic" in bsdf.inputs:
            bsdf.inputs["Metallic"].default_value = 0.0
        if "Subsurface Weight" in bsdf.inputs:
            bsdf.inputs["Subsurface Weight"].default_value = 0.0
        if emission and "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = (*emission, 1.0)
            bsdf.inputs["Emission Strength"].default_value = strength
    mat.diffuse_color = (*base, alpha)
    if alpha < 1.0:
        mat.blend_method = "BLEND"
        mat.use_screen_refraction = True
    return mat


def make_corian_mat(bpy):
    mat = bpy.data.materials.new("warm_white_translucent_crystalline_corian")
    mat.use_nodes = True
    nt = mat.node_tree
    nodes = nt.nodes
    links = nt.links
    bsdf = nodes.get("Principled BSDF")
    if not bsdf:
        return mat

    voronoi = nodes.new("ShaderNodeTexVoronoi")
    voronoi.inputs["Scale"].default_value = 22.0
    voronoi.inputs["Randomness"].default_value = 0.56
    if hasattr(voronoi, "feature"):
        voronoi.feature = "DISTANCE_TO_EDGE"
    if "Distance" in voronoi.inputs:
        voronoi.inputs["Distance"].default_value = 0.62

    cell_ramp = nodes.new("ShaderNodeValToRGB")
    cell_ramp.color_ramp.elements[0].position = 0.12
    cell_ramp.color_ramp.elements[0].color = (0.47, 0.45, 0.39, 1.0)
    cell_ramp.color_ramp.elements[1].position = 0.78
    cell_ramp.color_ramp.elements[1].color = (0.92, 0.86, 0.74, 1.0)
    links.new(voronoi.outputs["Distance"], cell_ramp.inputs["Fac"])
    links.new(cell_ramp.outputs["Color"], bsdf.inputs["Base Color"])

    noise = nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 115.0
    noise.inputs["Detail"].default_value = 13.0
    noise.inputs["Roughness"].default_value = 0.64

    bump = nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.038
    bump.inputs["Distance"].default_value = 0.42
    links.new(noise.outputs["Fac"], bump.inputs["Height"])
    links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])

    bsdf.inputs["Roughness"].default_value = 0.82
    if "Subsurface Weight" in bsdf.inputs:
        bsdf.inputs["Subsurface Weight"].default_value = 0.30
    if "Subsurface Radius" in bsdf.inputs:
        bsdf.inputs["Subsurface Radius"].default_value = (1.0, 0.68, 0.38)
    if "Emission Color" in bsdf.inputs:
        bsdf.inputs["Emission Color"].default_value = (1.0, 0.64, 0.30, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.006
    if "Alpha" in bsdf.inputs:
        bsdf.inputs["Alpha"].default_value = 0.92
    mat.diffuse_color = (0.86, 0.80, 0.68, 0.92)
    mat.blend_method = "BLEND"
    mat.use_screen_refraction = True
    return mat


def top_z_m(x_mm: float, y_mm: float) -> float:
    return z_surfaces(x_mm, y_mm)[1] * MM


def point_is_on_face(x_mm: float, y_mm: float, inset: float = 0.78) -> bool:
    a = LENGTH_MM / 2.0
    b = local_half_width(x_mm)
    if b <= 0:
        return False
    n = ((abs(x_mm) / a) ** SUPERELLIPSE_N + (abs(y_mm) / b) ** SUPERELLIPSE_N) ** (1.0 / SUPERELLIPSE_N)
    return n <= inset


def add_surface_curve(bpy, name: str, points_mm: list[tuple[float, float]], mat, bevel_mm: float):
    curve = bpy.data.curves.new(name, "CURVE")
    curve.dimensions = "3D"
    curve.resolution_u = 2
    curve.bevel_depth = bevel_mm * MM
    curve.bevel_resolution = 3
    spline = curve.splines.new("POLY")
    spline.points.add(len(points_mm) - 1)
    for point, (x_mm, y_mm) in zip(spline.points, points_mm):
        point.co = (x_mm * MM, y_mm * MM, top_z_m(x_mm, y_mm) + 0.33 * MM, 1.0)
    obj = bpy.data.objects.new(name, curve)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    return obj


def add_corian_luminous_mesh(bpy, pale_mat, glow_mat):
    """Visible surrogate for thinned Corian/KRION over a warm internal light pipe."""
    random.seed(7)

    for idx, y0 in enumerate([-20, -15, -10, -5, 0, 5, 10, 15, 20]):
        pts = []
        phase = idx * 0.71
        for step in range(104):
            x = -48.0 + step * 96.0 / 103.0
            y = y0 + 0.9 * math.sin(step * 0.13 + phase) + 0.35 * math.sin(step * 0.39)
            if point_is_on_face(x, y, 0.76):
                pts.append((x, y))
            elif len(pts) > 4:
                mat = glow_mat if idx in {2, 4, 6} else pale_mat
                add_surface_curve(bpy, f"subtle_corian_lattice_long_{idx}", pts, mat, 0.060 if mat == glow_mat else 0.030)
                pts = []
        if len(pts) > 4:
            mat = glow_mat if idx in {2, 4, 6} else pale_mat
            add_surface_curve(bpy, f"subtle_corian_lattice_long_{idx}", pts, mat, 0.060 if mat == glow_mat else 0.030)

    for idx, x0 in enumerate([-38, -28, -18, -8, 2, 12, 22, 32, 42]):
        pts = []
        phase = idx * 0.53
        for step in range(72):
            y = -24.0 + step * 48.0 / 71.0
            x = x0 + 0.8 * math.sin(step * 0.17 + phase)
            if point_is_on_face(x, y, 0.70):
                pts.append((x, y))
            elif len(pts) > 4:
                add_surface_curve(bpy, f"subtle_corian_lattice_cross_{idx}", pts, pale_mat, 0.026)
                pts = []
        if len(pts) > 4:
            add_surface_curve(bpy, f"subtle_corian_lattice_cross_{idx}", pts, pale_mat, 0.026)

    crescent = []
    for step in range(110):
        theta = math.radians(205 + step * 94 / 109)
        x = 43.0 * math.cos(theta) - 2.0
        y = 25.0 * math.sin(theta) - 1.5
        if point_is_on_face(x, y, 0.76):
            crescent.append((x, y))
    add_surface_curve(bpy, "warm_crescent_lightpipe_through_thinned_corian", crescent, glow_mat, 0.105)


def boundary_xy_mm(theta: float, side_scale: float = 1.0) -> tuple[float, float]:
    a = LENGTH_MM / 2.0
    c = math.cos(theta)
    sn = math.sin(theta)
    x = side_scale * a * math.copysign(abs(c) ** (2.0 / SUPERELLIPSE_N), c)
    local_b = local_half_width(x)
    y = side_scale * local_b * math.copysign(abs(sn) ** (2.0 / SUPERELLIPSE_N), sn)
    y = thumb_side_adjust(y)
    return organic_xy_adjust(x, y, side_scale)


def add_perimeter_glow_loop(bpy, name: str, mat, z_mm: float, scale: float, bevel_mm: float):
    curve = bpy.data.curves.new(name, "CURVE")
    curve.dimensions = "3D"
    curve.resolution_u = 3
    curve.bevel_depth = bevel_mm * MM
    curve.bevel_resolution = 8
    spline = curve.splines.new("POLY")
    spline.points.add(PERIMETER_SEGMENTS)
    for idx, point in enumerate(spline.points):
        theta = 2.0 * math.pi * (idx % PERIMETER_SEGMENTS) / PERIMETER_SEGMENTS
        x_mm, y_mm = boundary_xy_mm(theta, scale)
        point.co = (x_mm * MM, y_mm * MM, z_mm * MM, 1.0)
    obj = bpy.data.objects.new(name, curve)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    return obj


def add_flood_light_edge_seam(bpy, mat):
    """Quiet 60 mm side light seam that reads as an edge glow when active."""
    pts = []
    for idx in range(86):
        theta = math.radians(220 + idx * 100 / 85)
        x_mm, y_mm = boundary_xy_mm(theta, 0.955)
        pts.append((x_mm * MM, y_mm * MM, -6.9 * MM, 1.0))

    curve = bpy.data.curves.new("continuous_60mm_flood_light_edge_seam", "CURVE")
    curve.dimensions = "3D"
    curve.resolution_u = 4
    curve.bevel_depth = 0.28 * MM
    curve.bevel_resolution = 8
    spline = curve.splines.new("POLY")
    spline.points.add(len(pts) - 1)
    for point, co in zip(spline.points, pts):
        point.co = co
    obj = bpy.data.objects.new("continuous_60mm_flood_light_edge_seam", curve)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    return obj


def add_fibonacci_top_guide(bpy, mat):
    """Non-rendered construction guide: the flattened stone is derived from this spiral."""
    pts: list[tuple[float, float]] = []
    theta_max = math.radians(650)
    theta_min = math.radians(18)
    steps = 148
    for idx in range(steps):
        theta = theta_min + (theta_max - theta_min) * idx / (steps - 1)
        radius = 1.55 * (PHI ** (theta / (math.pi / 2.0)))
        x_mm = CROWN_OFFSET_X_MM + radius * math.cos(theta)
        y_mm = -3.0 + radius * math.sin(theta)
        if point_is_on_face(x_mm, y_mm, 0.70):
            pts.append((x_mm, y_mm))
    if len(pts) > 8:
        obj = add_surface_curve(bpy, "construction_fibonacci_spiral_flattened_nautilus_guide", pts, mat, 0.035)
        obj.hide_render = True
        obj.display_type = "WIRE"
        return obj
    return None


def add_bottom_flood_light_platform(bpy, strip_mat, reflector_mat):
    """Underside optics: two wide flood bands, one focused beam band, plus UV-A emitter."""
    z_reflector_mm = -(CENTER_THICKNESS_MM / 2.0 + BOTTOM_DISH_MM - 0.18)
    z_strip_mm = z_reflector_mm - 0.08
    created = []
    bands = [
        ("wide_flood_left", -14.0, 18.0, 4.2, 0.55),
        ("focused_flashlight_center", 0.0, 12.0, 2.4, 0.32),
        ("wide_flood_right", 14.0, 18.0, 4.2, 0.55),
    ]
    for idx, (role, y_mm, channel_width_mm, strip_width_mm, reflector_radius_mm) in enumerate(bands, start=1):
        reflector = add_box(
            bpy,
            f"{role}_parabolic_reflector_channel_{idx}_92mm",
            (92.0, channel_width_mm, 0.42),
            (0.0, y_mm * MM, z_reflector_mm * MM),
            reflector_mat,
        )
        reflector.modifiers["small_soft_radius"].width = reflector_radius_mm * MM
        created.append(reflector)
        strip = add_box(
            bpy,
            f"{role}_cob_led_band_{idx}_92mm_under_corian",
            (92.0, strip_width_mm, 0.18),
            (0.0, y_mm * MM, z_strip_mm * MM),
            strip_mat,
        )
        strip.modifiers["small_soft_radius"].width = 0.18 * MM
        created.append(strip)
        if role == "focused_flashlight_center":
            lens = add_box(
                bpy,
                "linear_prismatic_lens_over_focused_flashlight_band",
                (88.0, 5.0, 0.28),
                (0.0, y_mm * MM, (z_strip_mm - 0.22) * MM),
                strip_mat,
            )
            lens.modifiers["small_soft_radius"].width = 0.24 * MM
            created.append(lens)

    uv_mat = make_mat(bpy, "uv_a_inspection_emitters_365nm_violet_visible_proxy", (0.34, 0.18, 0.88), 0.28, 0.72, (0.32, 0.12, 1.0), 1.1)
    for idx, y_mm in enumerate([-24.0, 24.0], start=1):
        uv = add_cylinder_disc(
            bpy,
            f"uv_a_inspection_emitter_underbody_{idx}",
            2.2,
            0.20,
            (-46.0 * MM, y_mm * MM, (z_strip_mm - 0.18) * MM),
            uv_mat,
            48,
        )
        created.append(uv)

    for obj in created:
        # Present in the .blend for underside/engineering inspection, but not in the default top hero render.
        obj.hide_render = True


def add_internal_glow_volume(bpy, mat):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=96, ring_count=32, location=(CROWN_OFFSET_X_MM * MM, 0.0, 0.2 * MM))
    obj = bpy.context.object
    obj.name = "phi_crown_internal_amber_core_visible_through_corian"
    obj.scale = (31.0 * MM, 18.0 * MM, 2.8 * MM)
    obj.data.materials.append(mat)
    return obj


def add_table_glow_pool(bpy, mat):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=96, ring_count=16, location=(-2.0 * MM, 0.0, -9.52 * MM))
    obj = bpy.context.object
    obj.name = "soft_warm_reflection_pool_on_black_surface"
    obj.scale = (58.0 * MM, 38.0 * MM, 0.035 * MM)
    obj.data.materials.append(mat)
    return obj


def add_three_point_contact_pads(bpy, mat):
    """Three silicone-capped Corian datum feet placed as a golden gnomon."""
    center_z_mm = -(CENTER_THICKNESS_MM / 2.0 + BOTTOM_DISH_MM + FOOT_HEIGHT_MM / 2.0 + 0.08)
    for name, x_mm, y_mm, rot_deg in FOOT_POSITIONS_MM:
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=64,
            ring_count=16,
            location=(x_mm * MM, y_mm * MM, center_z_mm * MM),
            rotation=(0.0, 0.0, math.radians(rot_deg)),
        )
        obj = bpy.context.object
        obj.name = name
        obj.location.z = center_z_mm * MM
        obj.scale = (FOOT_RADIUS_MM * MM, FOOT_RADIUS_MM * MM, (FOOT_HEIGHT_MM / 2.0) * MM)
        obj.data.materials.append(mat)
        bevel = obj.modifiers.new("soft_polished_contact_edge", "BEVEL")
        bevel.width = 0.03 * MM
        bevel.segments = 5
    return None


def add_cylinder_disc(bpy, name, radius_mm, depth_mm, loc, mat, vertices=96):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices,
        radius=radius_mm * MM,
        depth=depth_mm * MM,
        location=loc,
        rotation=(0.0, 0.0, 0.0),
    )
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat)
    return obj


def add_box(bpy, name, size_mm, loc, mat):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = (size_mm[0] * MM, size_mm[1] * MM, size_mm[2] * MM)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    bevel = obj.modifiers.new("small_soft_radius", "BEVEL")
    bevel.width = 1.2 * MM
    bevel.segments = 8
    return obj


def clear_scene(bpy):
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    for collection in (bpy.data.meshes, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
        for block in list(collection):
            collection.remove(block)


def build_scene(passive=False, show_features=False, show_packaging=False, show_mesh=True, clay=False):
    import bpy

    clear_scene(bpy)
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    RENDER_DIR.mkdir(parents=True, exist_ok=True)

    krion = make_mat(bpy, "matte_clay_shape_review", (0.78, 0.74, 0.65), 0.9) if clay else make_corian_mat(bpy)
    amber = make_mat(bpy, "hidden_diffuse_amber_core_light", (1.0, 0.52, 0.18), 0.42, 0.10, (1.0, 0.42, 0.12), 0.0 if passive else 0.48)
    seam_glow = make_mat(bpy, "warm_amber_perimeter_light_channel", (1.0, 0.58, 0.20), 0.38, 0.58, (1.0, 0.42, 0.10), 0.0 if passive else 1.25)
    spiral_guide = make_mat(bpy, "non_rendered_phi_spiral_construction_guide", (0.72, 0.55, 0.20), 0.72, 0.38)
    flood_strip = make_mat(bpy, "bottom_cob_flood_strip_warm_white_active", (1.0, 0.95, 0.86), 0.36, 0.76, (1.0, 0.92, 0.78), 0.0 if passive else 1.7)
    reflector = make_mat(bpy, "polished_aluminum_parabolic_reflector_placeholder", (0.82, 0.80, 0.76), 0.08, 0.50)
    reflector_bsdf = reflector.node_tree.nodes.get("Principled BSDF")
    if reflector_bsdf and "Metallic" in reflector_bsdf.inputs:
        reflector_bsdf.inputs["Metallic"].default_value = 1.0
    sapphire = make_mat(bpy, "smoked_sapphire_ppg_window", (0.08, 0.11, 0.13), 0.08, 0.72)
    dark = make_mat(bpy, "soft_shadow_openings", (0.025, 0.022, 0.02), 0.8)
    guide_copper = make_mat(bpy, "engineering_copper_guide_hidden_by_default", (0.7, 0.38, 0.16), 0.38, 0.42)
    guide_magnet = make_mat(bpy, "engineering_magnet_guide_hidden_by_default", (0.52, 0.5, 0.46), 0.45, 0.38)

    verts, faces = build_body_mesh()
    mesh = bpy.data.meshes.new("EzraGoldenBodyMesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    body = bpy.data.objects.new("Ezra_116x64x15_phi_skip_stone_body", mesh)
    bpy.context.collection.objects.link(body)
    body.data.materials.append(krion)
    for poly in body.data.polygons:
        poly.use_smooth = True
    sub = body.modifiers.new("soft_surface_subdivision", "SUBSURF")
    sub.levels = 1
    sub.render_levels = 1
    add_three_point_contact_pads(bpy, krion)
    add_bottom_flood_light_platform(bpy, flood_strip, reflector)
    if show_mesh:
        add_internal_glow_volume(bpy, amber)
        add_perimeter_glow_loop(bpy, "concealed_0_6mm_midline_perimeter_light_channel", seam_glow, 0.12, 0.985, 0.085)
        add_perimeter_glow_loop(bpy, "soft_lower_edge_amber_bleed", seam_glow, -7.10, 0.942, 0.045)
        add_fibonacci_top_guide(bpy, spiral_guide)

    if show_features:
        add_cylinder_disc(bpy, "front_sapphire_ppg_eye_12mm", 6.0, 0.22, (-22.0 * MM, 0, 6.98 * MM), sapphire)
        add_box(bpy, "upper_hidden_speaker_slit_shadow", (32, 2.8, 0.22), (35.0 * MM, 0, 7.02 * MM), dark)
        add_box(bpy, "bottom_usb_c_port_shadow", (9, 0.38, 3.0), (-55.2 * MM, 0, 0), dark)

        for idx, (x, y) in enumerate([(-34, -21), (-34, 21), (34, -21), (34, 21)], start=1):
            add_cylinder_disc(bpy, f"mic_pinprick_phi_grid_{idx}", 0.42, 0.22, (x * MM, y * MM, 7.03 * MM), dark, 32)

    if show_packaging:
        add_cylinder_disc(bpy, "hidden_qi_magnet_envelope_56mm_engineering", 28.0, 0.35, (0, 0, -6.9 * MM), guide_magnet)
        add_cylinder_disc(bpy, "hidden_qi_coil_50mm_engineering", 25.0, 0.28, (0, 0, -7.2 * MM), guide_copper)
        add_box(bpy, "hidden_rear_thermal_presence_zone_40x40mm_engineering", (40, 40, 0.34), (-26.0 * MM, 0, -7.25 * MM), guide_copper)

    if not passive and show_mesh:
        for loc in [(-30, -15, 5.5), (-8, 2, 6.0), (18, 13, 5.5), (38, -10, 5.2)]:
            bpy.ops.object.light_add(type="POINT", location=(loc[0] * MM, loc[1] * MM, loc[2] * MM))
            light = bpy.context.object
            light.name = "warm_subsurface_point"
            light.data.color = (1.0, 0.68, 0.34)
            light.data.energy = 1.7

    bpy.context.scene.world = bpy.context.scene.world or bpy.data.worlds.new("World")
    bpy.context.scene.world.color = (0.022, 0.023, 0.022)

    bpy.ops.object.light_add(type="AREA", location=(0.0, -0.22, 0.17))
    key = bpy.context.object
    key.name = "large_softbox_key"
    key.data.energy = 5
    key.data.size = 0.32

    table_top_mm = -(CENTER_THICKNESS_MM / 2.0 + BOTTOM_DISH_MM + FOOT_HEIGHT_MM + 0.08)
    table_z_mm = table_top_mm - 1.0
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, table_z_mm * MM))
    desk = bpy.context.object
    desk.name = "matte_charcoal_table_plane"
    desk.dimensions = (2.40, 1.70, 0.002)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    desk.data.materials.append(make_mat(bpy, "matte_black_studio_surface", (0.004, 0.004, 0.004), 0.88))
    bpy.ops.object.camera_add(location=(0.112, -0.165, 0.058), rotation=(math.radians(67), 0, math.radians(36)))
    bpy.context.scene.camera = bpy.context.object
    bpy.context.object.name = "hero_camera"

    bpy.context.scene.render.engine = "CYCLES"
    bpy.context.scene.cycles.samples = 56
    bpy.context.scene.view_settings.exposure = -2.35
    bpy.context.scene.view_settings.gamma = 1.0
    bpy.context.scene.view_settings.view_transform = "Filmic"
    bpy.context.scene.render.resolution_x = 1200
    bpy.context.scene.render.resolution_y = 800
    return body


def set_camera(bpy, location, rotation_deg, lens=58):
    cam = bpy.context.scene.camera
    cam.location = location
    cam.rotation_euler = tuple(math.radians(v) for v in rotation_deg)
    cam.data.lens = lens


def render_scene_variants(bpy):
    variants = [
        ("hero_internal_glow.png", (0.13, -0.19, 0.085), (64, 0, 37), -2.2, 58),
        ("morning_guidance_bedside.png", (0.02, -0.18, 0.115), (58, 0, 6), -2.0, 64),
        ("pre_meeting_calm_haptic.png", (0.145, -0.13, 0.075), (63, 0, 48), -2.15, 70),
        ("evening_wind_down_amber.png", (-0.02, -0.16, 0.09), (61, 0, -8), -2.35, 62),
        ("walk_prompt_subtle_pulse.png", (0.10, -0.21, 0.072), (66, 0, 28), -2.1, 58),
        ("emotional_recovery_warmth.png", (-0.115, -0.17, 0.083), (63, 0, -34), -2.3, 64),
    ]
    for filename, loc, rot, exposure, lens in variants:
        set_camera(bpy, loc, rot, lens)
        bpy.context.scene.view_settings.exposure = exposure
        bpy.context.scene.render.filepath = str(RENDER_DIR / filename)
        bpy.ops.render.render(write_still=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--save-blend", action="store_true")
    parser.add_argument("--export-all", action="store_true")
    parser.add_argument("--render-hero", action="store_true")
    parser.add_argument("--render-scenes", action="store_true")
    parser.add_argument("--passive", action="store_true")
    parser.add_argument("--show-features", action="store_true")
    parser.add_argument("--show-packaging", action="store_true")
    parser.add_argument("--no-mesh", action="store_true")
    parser.add_argument("--clay", action="store_true")
    script_args = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    args = parser.parse_args(script_args)

    import bpy

    build_scene(
        passive=args.passive,
        show_features=args.show_features,
        show_packaging=args.show_packaging,
        show_mesh=not args.no_mesh,
        clay=args.clay,
    )

    if args.save_blend:
        bpy.ops.wm.save_as_mainfile(filepath=str(OUT_DIR / "ezra_golden_phone.blend"))
    if args.export_all:
        bpy.ops.wm.obj_export(filepath=str(EXPORT_DIR / "ezra_golden_phone.obj"))
        if hasattr(bpy.ops.wm, "stl_export"):
            bpy.ops.wm.stl_export(filepath=str(EXPORT_DIR / "ezra_golden_phone.stl"))
        elif hasattr(bpy.ops.export_mesh, "stl"):
            bpy.ops.export_mesh.stl(filepath=str(EXPORT_DIR / "ezra_golden_phone.stl"))
        bpy.ops.export_scene.gltf(filepath=str(EXPORT_DIR / "ezra_golden_phone.glb"), export_format="GLB")
    if args.render_hero:
        bpy.context.scene.render.filepath = str(RENDER_DIR / "skip_stone_glow_target.png")
        bpy.ops.render.render(write_still=True)
    if args.render_scenes:
        render_scene_variants(bpy)


if __name__ == "__main__":
    main()
