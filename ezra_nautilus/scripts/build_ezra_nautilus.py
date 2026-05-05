#!/usr/bin/env python3
"""
Ezra — Nautilus shell v2 (procedural approximation).

  blender --background --python ezra_nautilus/scripts/build_ezra_nautilus.py -- [args]

  --save-blend    ezra_nautilus/ezra_nautilus.blend
  --export-all    exports/ezra_nautilus.{obj,stl,glb}
  --render-hero   hero_convex only
  --render-all    all named cameras (slow)
  --turntable     72 frames, orbit cam 25° elevation
  --passive       emission strengths → 0 (technical pass)

Silhouette: symmetric ~93×80 mm crescent; thickness 14→28 mm (curl→top arc);
convex bulge + concave bowl + 8 spiral-twisted radial ribs (see BRIEF.md).
"""

from __future__ import annotations

import argparse
import math
import os
import sys

MM = 0.001

# Symmetric half-moon outline (mm), origin geometric center, CCW
SIL_MM = [
    (0.0, -40.0),
    (-20.0, -39.5),
    (-40.0, -31.0),
    (-46.5, -14.0),
    (-46.5, 14.0),
    (-40.0, 31.0),
    (-22.0, 38.5),
    (0.0, 40.0),
    (22.0, 38.5),
    (40.0, 31.0),
    (46.5, 14.0),
    (46.5, -14.0),
    (40.0, -31.0),
    (20.0, -39.5),
]

CURL_X_MM = 0.0
CURL_Y_MM = -38.5

THICK_LO_MM = 14.0
THICK_HI_MM = 28.0
RIB_COUNT = 8

USB_W_MM = 9.0
USB_H_MM = 3.5
LASER_D_MM = 3.0
SENSOR_D_MM = 14.0
SENSOR_DEPTH_MM = 2.2
SENSOR_Y_MM = -10.0  # ~30 mm “up” from curl toward top

GRID_STEP_MM = 1.35
X_RANGE = (-47.5, 47.5)
Y_RANGE = (-41.5, 41.5)


def _bpy():
    import bpy  # noqa: WPS433

    return bpy


def smoothstep(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


def point_in_poly(x: float, y: float, poly: list[tuple[float, float]]) -> bool:
    n = len(poly)
    inside = False
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > y) != (yj > y)) and (
            x < (xj - xi) * (y - yi) / (yj - yi + 1e-15) + xi
        ):
            inside = not inside
        j = i
    return inside


def thickness_mm(y_mm: float) -> float:
    u = (y_mm + 40.0) / 80.0
    return THICK_LO_MM + smoothstep(u) * (THICK_HI_MM - THICK_LO_MM)


def concave_mm(x_mm: float, y_mm: float) -> float:
    return -4.0 * math.exp(-((x_mm / 28.0) ** 2 + ((y_mm + 30.0) / 18.0) ** 2))


def convex_mm(x_mm: float, y_mm: float) -> float:
    return 8.0 * math.exp(-((x_mm / 32.0) ** 2 + ((y_mm - 4.0) / 38.0) ** 2))


def rib_mm(x_mm: float, y_mm: float) -> float:
    dx = x_mm - CURL_X_MM
    dy = y_mm - CURL_Y_MM
    r = math.hypot(dx, dy) + 1e-6
    theta = math.atan2(dy, dx)
    theta_s = theta + 0.42 * math.log(r / 12.0 + 1.0)
    env = smoothstep(min(1.0, r / 52.0))
    h_env = 1.5 + env * (3.5 - 1.5)
    crest = max(0.0, math.cos(RIB_COUNT * theta_s)) ** 10
    return h_env * crest


def z_surfaces_mm(x_mm: float, y_mm: float) -> tuple[float, float]:
    zb = concave_mm(x_mm, y_mm)
    zt = zb + thickness_mm(y_mm) + convex_mm(x_mm, y_mm) + rib_mm(x_mm, y_mm)
    return zb, zt


def build_vertices_and_faces():
    xmin, xmax = X_RANGE
    ymin, ymax = Y_RANGE
    dx = GRID_STEP_MM
    nx = int(round((xmax - xmin) / dx)) + 1
    ny = int(round((ymax - ymin) / dx)) + 1
    dx = (xmax - xmin) / max(nx - 1, 1)
    dy = (ymax - ymin) / max(ny - 1, 1)

    inside: list[list[bool]] = []
    for j in range(ny):
        row = []
        y_mm = ymin + j * dy
        for i in range(nx):
            x_mm = xmin + i * dx
            row.append(point_in_poly(x_mm, y_mm, SIL_MM))
        inside.append(row)

    verts: list[tuple[float, float, float]] = []
    gb = [[-1] * nx for _ in range(ny)]
    gt = [[-1] * nx for _ in range(ny)]

    for j in range(ny):
        for i in range(nx):
            if not inside[j][i]:
                continue
            x_mm = xmin + i * dx
            y_mm = ymin + j * dy
            zb, zt = z_surfaces_mm(x_mm, y_mm)
            gb[j][i] = len(verts)
            verts.append((x_mm * MM, y_mm * MM, zb * MM))
            gt[j][i] = len(verts)
            verts.append((x_mm * MM, y_mm * MM, zt * MM))

    faces: list[tuple[int, ...]] = []

    for j in range(ny - 1):
        for i in range(nx - 1):
            if not (
                inside[j][i]
                and inside[j][i + 1]
                and inside[j + 1][i + 1]
                and inside[j + 1][i]
            ):
                continue
            faces.append((gt[j][i], gt[j][i + 1], gt[j + 1][i + 1], gt[j + 1][i]))
            faces.append((gb[j][i], gb[j + 1][i], gb[j + 1][i + 1], gb[j][i + 1]))

    # Skirts: vertical edges between columns (constant x wall)
    for j in range(ny - 1):
        for i in range(nx - 1):
            a = inside[j][i]
            b = inside[j][i + 1]
            if a == b:
                continue
            x_wall = xmin + (i + 1) * dx
            side = 1 if a else -1
            x_samp = x_wall - side * 0.07
            y0 = ymin + j * dy
            y1 = ymin + (j + 1) * dy
            zb0, zt0 = z_surfaces_mm(x_samp, y0)
            zb1, zt1 = z_surfaces_mm(x_samp, y1)
            x_wm = x_wall * MM
            i0 = len(verts)
            verts.extend(
                [
                    (x_wm, y0 * MM, zb0 * MM),
                    (x_wm, y1 * MM, zb1 * MM),
                    (x_wm, y1 * MM, zt1 * MM),
                    (x_wm, y0 * MM, zt0 * MM),
                ]
            )
            if side > 0:
                faces.append((i0, i0 + 1, i0 + 2, i0 + 3))
            else:
                faces.append((i0, i0 + 3, i0 + 2, i0 + 1))

    # Horizontal edges between rows (constant y wall)
    for j in range(ny - 1):
        for i in range(nx - 1):
            a = inside[j][i]
            b = inside[j + 1][i]
            if a == b:
                continue
            y_wall = ymin + (j + 1) * dy
            side = 1 if a else -1
            y_samp = y_wall - side * 0.07
            x0 = xmin + i * dx
            x1 = xmin + (i + 1) * dx
            zb0, zt0 = z_surfaces_mm(x0, y_samp)
            zb1, zt1 = z_surfaces_mm(x1, y_samp)
            y_wm = y_wall * MM
            i0 = len(verts)
            verts.extend(
                [
                    (x0 * MM, y_wm, zb0 * MM),
                    (x1 * MM, y_wm, zb1 * MM),
                    (x1 * MM, y_wm, zt1 * MM),
                    (x0 * MM, y_wm, zt0 * MM),
                ]
            )
            if side > 0:
                faces.append((i0, i0 + 1, i0 + 2, i0 + 3))
            else:
                faces.append((i0, i0 + 3, i0 + 2, i0 + 1))

    return verts, faces


def clear_scene(bpy):
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for block in list(bpy.data.meshes):
        bpy.data.meshes.remove(block)
    for block in list(bpy.data.materials):
        bpy.data.materials.remove(block)
    for block in list(bpy.data.cameras):
        bpy.data.cameras.remove(block)
    for block in list(bpy.data.lights):
        bpy.data.lights.remove(block)


def rgb_norm(r, g, b):
    return (r / 255.0, g / 255.0, b / 255.0)


def mat_krion_nautilus(bpy, passive: bool):
    """Single KRION: procedural valley vs crest + convex-side emission."""
    mat = bpy.data.materials.new("KRION_Nautilus")
    mat.use_nodes = True
    nt = mat.node_tree
    nodes = nt.nodes
    links = nt.links
    nodes.clear()

    out = nodes.new("ShaderNodeOutputMaterial")

    geo = nodes.new("ShaderNodeNewGeometry")
    texco = nodes.new("ShaderNodeTexCoord")
    sep = nodes.new("ShaderNodeSeparateXYZ")
    links.new(texco.outputs["Object"], sep.inputs["Vector"])

    curl_dy = nodes.new("ShaderNodeMath")
    curl_dy.operation = "SUBTRACT"
    links.new(sep.outputs["Y"], curl_dy.inputs[0])
    curl_dy.inputs[1].default_value = CURL_Y_MM * MM

    ang = nodes.new("ShaderNodeMath")
    ang.operation = "ARCTAN2"
    links.new(curl_dy.outputs["Value"], ang.inputs[0])
    links.new(sep.outputs["X"], ang.inputs[1])

    rad_xy = nodes.new("ShaderNodeCombineXYZ")
    links.new(sep.outputs["X"], rad_xy.inputs["X"])
    links.new(curl_dy.outputs["Value"], rad_xy.inputs["Y"])
    rad_xy.inputs["Z"].default_value = 0.0
    len_xy = nodes.new("ShaderNodeVectorMath")
    len_xy.operation = "LENGTH"
    links.new(rad_xy.outputs["Vector"], len_xy.inputs[0])

    logr = nodes.new("ShaderNodeMath")
    logr.operation = "LOGARITHM"
    r_eps = nodes.new("ShaderNodeMath")
    r_eps.operation = "ADD"
    links.new(len_xy.outputs["Value"], r_eps.inputs[0])
    r_eps.inputs[1].default_value = 12.0 * MM
    links.new(r_eps.outputs["Value"], logr.inputs[0])

    mul_sc = nodes.new("ShaderNodeMath")
    mul_sc.operation = "MULTIPLY"
    links.new(logr.outputs["Value"], mul_sc.inputs[0])
    mul_sc.inputs[1].default_value = 0.42

    theta_s = nodes.new("ShaderNodeMath")
    theta_s.operation = "ADD"
    links.new(ang.outputs["Value"], theta_s.inputs[0])
    links.new(mul_sc.outputs["Value"], theta_s.inputs[1])

    rib_wave = nodes.new("ShaderNodeMath")
    rib_wave.operation = "COSINE"
    mul8 = nodes.new("ShaderNodeMath")
    mul8.operation = "MULTIPLY"
    mul8.inputs[1].default_value = float(RIB_COUNT)
    links.new(theta_s.outputs["Value"], mul8.inputs[0])
    links.new(mul8.outputs["Value"], rib_wave.inputs[0])

    cos_pos = nodes.new("ShaderNodeMath")
    cos_pos.operation = "MAXIMUM"
    links.new(rib_wave.outputs["Value"], cos_pos.inputs[0])
    cos_pos.inputs[1].default_value = 0.0

    crest = nodes.new("ShaderNodeMath")
    crest.operation = "POWER"
    crest.inputs[1].default_value = 7.0
    links.new(cos_pos.outputs["Value"], crest.inputs[0])

    valley = nodes.new("ShaderNodeMath")
    valley.operation = "SUBTRACT"
    valley.inputs[0].default_value = 1.0
    links.new(crest.outputs["Value"], valley.inputs[1])

    rough_mix = nodes.new("ShaderNodeMixRGB")
    rough_mix.blend_type = "MIX"
    links.new(valley.outputs["Value"], rough_mix.inputs["Fac"])
    rough_mix.inputs["Color1"].default_value = (0.65, 0.65, 0.65, 1.0)
    rough_mix.inputs["Color2"].default_value = (0.15, 0.15, 0.15, 1.0)

    spec_mix = nodes.new("ShaderNodeMixRGB")
    links.new(valley.outputs["Value"], spec_mix.inputs["Fac"])
    spec_mix.inputs["Color1"].default_value = (0.08, 0.08, 0.08, 1.0)
    spec_mix.inputs["Color2"].default_value = (0.35, 0.35, 0.35, 1.0)

    vor = nodes.new("ShaderNodeTexVoronoi")
    vor.feature = "DISTANCE_TO_EDGE"
    vor.distance = "EUCLIDEAN"
    vor.inputs["Scale"].default_value = 2.8
    mapping = nodes.new("ShaderNodeMapping")
    links.new(texco.outputs["Object"], mapping.inputs["Vector"])
    links.new(mapping.outputs["Vector"], vor.inputs["Vector"])

    ramp = nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.42
    ramp.color_ramp.elements[1].position = 0.9
    ramp.color_ramp.elements[0].color = (*rgb_norm(248, 245, 240), 1.0)
    ramp.color_ramp.elements[1].color = (*rgb_norm(200, 194, 185), 1.0)
    links.new(vor.outputs["Distance"], ramp.inputs["Fac"])

    mix_vein = nodes.new("ShaderNodeMixRGB")
    mix_vein.blend_type = "MIX"
    mix_vein.inputs["Fac"].default_value = 0.28
    mix_vein.inputs["Color1"].default_value = (*rgb_norm(248, 245, 240), 1.0)
    links.new(ramp.outputs["Color"], mix_vein.inputs["Color2"])

    principled = nodes.new("ShaderNodeBsdfPrincipled")
    links.new(mix_vein.outputs["Color"], principled.inputs["Base Color"])
    links.new(rough_mix.outputs["Color"], principled.inputs["Roughness"])
    if "Specular IOR Level" in principled.inputs:
        links.new(spec_mix.outputs["Color"], principled.inputs["Specular IOR Level"])
    elif "Specular" in principled.inputs:
        links.new(spec_mix.outputs["Color"], principled.inputs["Specular"])
    if "IOR" in principled.inputs:
        principled.inputs["IOR"].default_value = 1.48

    if "Subsurface Weight" in principled.inputs:
        principled.inputs["Subsurface Weight"].default_value = 0.38
        principled.inputs["Subsurface Radius"].default_value = (1.2, 1.0, 0.8)
    elif "Subsurface" in principled.inputs:
        principled.inputs["Subsurface"].default_value = 0.38
        principled.inputs["Subsurface Radius"].default_value = (0.0013, 0.0011, 0.0009)

    curl_bias = nodes.new("ShaderNodeMath")
    curl_bias.operation = "LESS_THAN"
    links.new(len_xy.outputs["Value"], curl_bias.inputs[0])
    curl_bias.inputs[1].default_value = 0.019

    sep_n = nodes.new("ShaderNodeSeparateXYZ")
    links.new(geo.outputs["Normal"], sep_n.inputs["Vector"])
    facing = nodes.new("ShaderNodeMath")
    facing.operation = "GREATER_THAN"
    links.new(sep_n.outputs["Z"], facing.inputs[0])
    facing.inputs[1].default_value = 0.26

    chamber_fac = nodes.new("ShaderNodeMath")
    chamber_fac.operation = "MULTIPLY"
    links.new(valley.outputs["Value"], chamber_fac.inputs[0])
    links.new(facing.outputs["Value"], chamber_fac.inputs[1])

    cu_part = nodes.new("ShaderNodeMath")
    cu_part.operation = "MULTIPLY"
    links.new(curl_bias.outputs["Value"], cu_part.inputs[0])
    links.new(facing.outputs["Value"], cu_part.inputs[1])

    z_pass = nodes.new("ShaderNodeValue")
    z_pass.outputs[0].default_value = 0.0 if passive else 1.0

    ch_a = nodes.new("ShaderNodeMath")
    ch_a.operation = "MULTIPLY"
    links.new(chamber_fac.outputs["Value"], ch_a.inputs[0])
    links.new(z_pass.outputs["Value"], ch_a.inputs[1])

    ch_strength = nodes.new("ShaderNodeMath")
    ch_strength.operation = "MULTIPLY"
    links.new(ch_a.outputs["Value"], ch_strength.inputs[0])
    ch_strength.inputs[1].default_value = 1.4

    cu_a = nodes.new("ShaderNodeMath")
    cu_a.operation = "MULTIPLY"
    links.new(cu_part.outputs["Value"], cu_a.inputs[0])
    links.new(z_pass.outputs["Value"], cu_a.inputs[1])

    cu_strength = nodes.new("ShaderNodeMath")
    cu_strength.operation = "MULTIPLY"
    links.new(cu_a.outputs["Value"], cu_strength.inputs[0])
    cu_strength.inputs[1].default_value = 2.2

    emit_chamber = nodes.new("ShaderNodeEmission")
    emit_chamber.inputs["Color"].default_value = (*rgb_norm(255, 248, 228), 1.0)
    links.new(ch_strength.outputs["Value"], emit_chamber.inputs["Strength"])

    emit_curl = nodes.new("ShaderNodeEmission")
    emit_curl.inputs["Color"].default_value = (*rgb_norm(255, 190, 120), 1.0)
    links.new(cu_strength.outputs["Value"], emit_curl.inputs["Strength"])

    add_em = nodes.new("ShaderNodeAddShader")
    links.new(emit_chamber.outputs["Emission"], add_em.inputs[0])
    links.new(emit_curl.outputs["Emission"], add_em.inputs[1])

    add_all = nodes.new("ShaderNodeAddShader")
    links.new(principled.outputs["BSDF"], add_all.inputs[0])
    links.new(add_em.outputs["Shader"], add_all.inputs[1])

    links.new(add_all.outputs["Shader"], out.inputs["Surface"])

    return mat


def bool_diff(bpy, target, cutter_name: str, verts, faces):
    cm = bpy.data.meshes.new(cutter_name + "_m")
    cm.from_pydata(verts, [], faces)
    cm.update()
    cutter = bpy.data.objects.new(cutter_name, cm)
    bpy.context.collection.objects.link(cutter)
    mod = target.modifiers.new(name=cutter_name, type="BOOLEAN")
    mod.operation = "DIFFERENCE"
    mod.object = cutter
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=cutter.name)
    bpy.data.objects.remove(cutter, do_unlink=True)
    bpy.data.meshes.remove(cm)


def _box(hx, hy, hz, cx, cy, cz):
    v = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            for sz in (-1, 1):
                v.append((cx + sx * hx, cy + sy * hy, cz + sz * hz))
    f = [
        (0, 1, 3, 2),
        (6, 7, 5, 4),
        (0, 2, 6, 4),
        (3, 1, 5, 7),
        (2, 3, 7, 6),
        (4, 5, 1, 0),
    ]
    return v, f


def apply_features(bpy, obj):
    """USB + laser + dual-face sensor + mirrored speaker slots."""
    _, zt_sensor = z_surfaces_mm(0.0, SENSOR_Y_MM)
    sx, sy = 0.0, SENSOR_Y_MM * MM

    bpy.ops.mesh.primitive_cylinder_add(
        radius=(SENSOR_D_MM * 0.5) * MM,
        depth=SENSOR_DEPTH_MM * MM * 3,
        location=(sx, sy, zt_sensor * MM + SENSOR_DEPTH_MM * MM),
        rotation=(0.0, 0.0, 0.0),
    )
    c = bpy.context.active_object
    c.name = "CutSensorTop"
    mod = obj.modifiers.new(name="CutSensorTop", type="BOOLEAN")
    mod.operation = "DIFFERENCE"
    mod.object = c
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier="CutSensorTop")
    bpy.data.objects.remove(c, do_unlink=True)

    zb_bot = concave_mm(0.0, SENSOR_Y_MM) * MM
    bpy.ops.mesh.primitive_cylinder_add(
        radius=(SENSOR_D_MM * 0.5) * MM,
        depth=SENSOR_DEPTH_MM * MM * 3,
        location=(sx, sy, zb_bot - SENSOR_DEPTH_MM * MM * 1.5),
        rotation=(0.0, 0.0, 0.0),
    )
    c2 = bpy.context.active_object
    c2.name = "CutSensorBot"
    mod = obj.modifiers.new(name="CutSensorBot", type="BOOLEAN")
    mod.operation = "DIFFERENCE"
    mod.object = c2
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier="CutSensorBot")
    bpy.data.objects.remove(c2, do_unlink=True)

    usb_z = (concave_mm(0.0, CURL_Y_MM) + thickness_mm(CURL_Y_MM) * 0.35) * MM
    uw, uh = USB_W_MM * MM * 0.5, USB_H_MM * MM * 0.5
    dv, df = _box(uw, uh, 6 * MM, 0.0, CURL_Y_MM * MM, usb_z)
    bool_diff(bpy, obj, "CutUSB", dv, df)

    bpy.ops.mesh.primitive_cylinder_add(
        radius=(LASER_D_MM * 0.5) * MM,
        depth=THICK_HI_MM * MM * 2,
        location=(0.0, CURL_Y_MM * MM, usb_z),
        rotation=(math.pi / 2, 0.0, 0.0),
    )
    lz = bpy.context.active_object
    mod = obj.modifiers.new(name="CutLaser", type="BOOLEAN")
    mod.operation = "DIFFERENCE"
    mod.object = lz
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier="CutLaser")
    bpy.data.objects.remove(lz, do_unlink=True)

    sy_sp = 28.0 * MM
    for side_sign in (-1.0, 1.0):
        cx = side_sign * (46.5 * MM - 5 * MM)
        cz_mid = (concave_mm(cx / MM, sy_sp / MM) + z_surfaces_mm(cx / MM, sy_sp / MM)[1]) * 0.5 * MM
        hv, hf = _box(10 * MM, 6 * MM, 4 * MM, cx, sy_sp, cz_mid)
        bool_diff(bpy, obj, f"CutSpeaker{side_sign:g}", hv, hf)


def add_pedestal_and_lights(bpy):
    bpy.ops.mesh.primitive_plane_add(size=0.65, location=(0.0, 0.0, -0.028))
    pl = bpy.context.active_object
    pl.name = "Pedestal"
    pm = bpy.data.materials.new("PedestalDark")
    pm.use_nodes = True
    nt = pm.node_tree
    nt.nodes.clear()
    o = nt.nodes.new("ShaderNodeOutputMaterial")
    p = nt.nodes.new("ShaderNodeBsdfPrincipled")
    p.inputs["Base Color"].default_value = (0.025, 0.024, 0.022, 1.0)
    p.inputs["Roughness"].default_value = 0.06
    nt.links.new(p.outputs["BSDF"], o.inputs["Surface"])
    pl.data.materials.append(pm)

    bpy.ops.object.light_add(type="AREA", location=(-0.4, -0.35, 0.35))
    k = bpy.context.active_object
    k.data.energy = 120
    k.data.size = 2.0

    bpy.ops.object.light_add(type="AREA", location=(0.35, 0.25, -0.08))
    f = bpy.context.active_object
    f.data.energy = 40
    f.data.size = 1.5


def camera_track_world_center(obj):
    from mathutils import Vector

    acc = Vector((0.0, 0.0, 0.0))
    for corner in obj.bound_box:
        acc += obj.matrix_world @ Vector(corner)
    return acc / 8.0


def scene_scale_from_body(obj, ref_span_mm: float = 93.0) -> float:
    span = max(max(obj.dimensions.x, obj.dimensions.y), obj.dimensions.z, 1e-9)
    return span / (ref_span_mm * MM)


def configure_camera_clip(cam_ob, clip_end: float = 12.0):
    cam_ob.data.clip_start = 0.002
    cam_ob.data.clip_end = clip_end


def add_empty(bpy, name, loc):
    e = bpy.data.objects.new(name, None)
    e.empty_display_type = "PLAIN_AXES"
    e.empty_display_size = 0.018
    e.location = loc
    bpy.context.collection.objects.link(e)
    return e


def add_camera_track(bpy, name, loc, tgt):
    cd = bpy.data.cameras.new(name)
    ob = bpy.data.objects.new(name, cd)
    bpy.context.collection.objects.link(ob)
    ob.location = loc
    con = ob.constraints.new(type="TRACK_TO")
    con.target = tgt
    con.track_axis = "TRACK_NEGATIVE_Z"
    con.up_axis = "UP_Y"
    return ob


def setup_cameras(bpy, tgt, scale: float = 1.0):
    d = 0.42 * scale
    specs = {
        "hero_convex": (0.28 * scale, -0.32 * scale, d * 0.85),
        "hero_curl": (0.05 * scale, 0.08 * scale, -d * 0.55),
        "profile_side": (-d * 1.2, 0.02 * scale, 0.06 * scale),
        "desk_resting": (0.35 * scale, -0.38 * scale, d * 0.45),
        "in_hand_right": (-d * 0.55, -d * 0.95, 0.12 * scale),
        "in_hand_left": (d * 0.55, -d * 0.95, 0.12 * scale),
        "fibonacci_sequence": (0.02 * scale, 0.02 * scale, d * 1.05),
        "macro_rib": (-0.06 * scale, -0.02 * scale, 0.052 * scale),
        "macro_sensor": (-0.045 * scale, SENSOR_Y_MM * MM - 0.018 * scale, 0.065 * scale),
    }
    for nm, loc in specs.items():
        cam_ob = add_camera_track(bpy, nm, loc, tgt)
        configure_camera_clip(cam_ob)


def render_configure(
    bpy,
    transparent: bool,
    dark_bg: bool,
    *,
    cycles_samples: int | None = None,
    resolution_percentage: int = 100,
):
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.samples = cycles_samples if cycles_samples is not None else 224
    sc.render.resolution_x = 4000
    sc.render.resolution_y = 4000
    sc.render.resolution_percentage = max(1, min(100, resolution_percentage))
    sc.render.film_transparent = transparent
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA" if transparent else "RGB"

    world = bpy.data.worlds.new("WorldNautilus")
    sc.world = world
    world.use_nodes = True
    nt = world.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputWorld")
    bg = nt.nodes.new("ShaderNodeBackground")
    if dark_bg:
        bg.inputs["Color"].default_value = (0.039, 0.039, 0.031, 1.0)
        bg.inputs["Strength"].default_value = 0.06 if not transparent else 0.0
    else:
        bg.inputs["Color"].default_value = (0.95, 0.93, 0.90, 1.0)
        bg.inputs["Strength"].default_value = 0.45
    nt.links.new(bg.outputs["Background"], out.inputs["Surface"])


def save_blend(bpy, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=path)


def export_all(bpy, root: str):
    exp = os.path.join(root, "exports")
    os.makedirs(exp, exist_ok=True)
    bpy.ops.object.select_all(action="DESELECT")
    ob = bpy.data.objects["EzraBody"]
    ob.select_set(True)
    bpy.context.view_layer.objects.active = ob
    base = os.path.join(exp, "ezra_nautilus")
    bpy.ops.wm.obj_export(filepath=base + ".obj", export_selected_objects=True)
    try:
        bpy.ops.wm.stl_export(filepath=base + ".stl", export_selected_objects=True)
    except Exception:
        pass
    try:
        bpy.ops.export_scene.gltf(filepath=base + ".glb", export_format="GLB", use_selection=True)
    except Exception:
        pass


def render_names(bpy, root: str, names: list[str], transparent: bool, dark: bool):
    render_configure(bpy, transparent, dark)
    rnd = os.path.join(root, "renders")
    os.makedirs(rnd, exist_ok=True)
    sc = bpy.context.scene
    for nm in names:
        cam = bpy.data.objects.get(nm)
        if not cam:
            continue
        sc.camera = cam
        sc.render.filepath = os.path.join(rnd, nm + ".png")
        bpy.ops.render.render(write_still=True)


def turntable(
    bpy,
    root,
    body,
    *,
    frames: int = 72,
    elevation_deg: float = 25.0,
    cycles_samples: int | None = None,
    resolution_percentage: int = 100,
):
    """Orbit TurntableCam around CamTarget at fixed elevation (spec §9)."""
    render_configure(
        bpy,
        False,
        True,
        cycles_samples=cycles_samples,
        resolution_percentage=resolution_percentage,
    )
    sc = bpy.context.scene
    tgt = bpy.data.objects.get("CamTarget")
    if tgt is None:
        raise RuntimeError("turntable: CamTarget missing")

    span = max(max(body.dimensions.x, body.dimensions.y), body.dimensions.z, 1e-9)
    dist = max(span * 0.62, 0.28)

    el = math.radians(elevation_deg)
    cd = bpy.data.cameras.new("TurntableCam")
    cob = bpy.data.objects.new("TurntableCam", cd)
    bpy.context.collection.objects.link(cob)
    configure_camera_clip(cob)
    sc.camera = cob
    con = cob.constraints.new(type="TRACK_TO")
    con.target = tgt
    con.track_axis = "TRACK_NEGATIVE_Z"
    con.up_axis = "UP_Y"
    tt = os.path.join(root, "turntable")
    os.makedirs(tt, exist_ok=True)
    body.rotation_mode = "XYZ"
    z0 = body.rotation_euler[2]
    n = max(1, frames)
    for i in range(n):
        az = math.radians(i * (360.0 / n))
        x = dist * math.cos(el) * math.sin(az)
        z = dist * math.cos(el) * math.cos(az)
        y = dist * math.sin(el)
        cob.location = (x, -z, y)
        bpy.context.view_layer.update()
        sc.render.filepath = os.path.join(tt, f"frame_{i:03d}.png")
        bpy.ops.render.render(write_still=True)
    body.rotation_euler[2] = z0


def parse_argv():
    if "--" in sys.argv:
        i = sys.argv.index("--")
        raw = sys.argv[i + 1 :]
    else:
        raw = []
    p = argparse.ArgumentParser()
    p.add_argument("--save-blend", action="store_true")
    p.add_argument("--export-all", action="store_true")
    p.add_argument("--render-hero", action="store_true")
    p.add_argument("--render-all", action="store_true")
    p.add_argument("--turntable", action="store_true")
    p.add_argument(
        "--turntable-quick",
        action="store_true",
        help="QA: 8 frames, 25%% res, 20 samples (fast)",
    )
    p.add_argument("--passive", action="store_true")
    return p.parse_args(raw)


def main():
    args = parse_argv()
    bpy = _bpy()
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    clear_scene(bpy)
    verts, faces = build_vertices_and_faces()
    mesh = bpy.data.meshes.new("EzraNautilus")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new("EzraBody", mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.shade_smooth()

    obj.data.materials.append(mat_krion_nautilus(bpy, passive=args.passive))

    apply_features(bpy, obj)

    if not any(m.type == "WEIGHTED_NORMAL" for m in obj.modifiers):
        wn = obj.modifiers.new(name="WeightedNormal", type="WEIGHTED_NORMAL")
        wn.keep_sharp = True

    ctr = camera_track_world_center(obj)
    tgt = add_empty(bpy, "CamTarget", ctr)
    sf = scene_scale_from_body(obj)
    setup_cameras(bpy, tgt, scale=max(sf, 0.92))
    add_pedestal_and_lights(bpy)

    blend_path = os.path.join(root, "ezra_nautilus.blend")
    if args.save_blend:
        save_blend(bpy, blend_path)
    if args.export_all:
        export_all(bpy, root)
    if args.render_hero:
        render_names(bpy, root, ["hero_convex"], transparent=True, dark=True)
    if args.render_all:
        render_names(
            bpy,
            root,
            list(
                {
                    "hero_convex",
                    "hero_curl",
                    "profile_side",
                    "desk_resting",
                    "in_hand_right",
                    "in_hand_left",
                    "fibonacci_sequence",
                    "macro_rib",
                    "macro_sensor",
                }
            ),
            transparent=True,
            dark=True,
        )
    if args.turntable_quick:
        turntable(
            bpy,
            root,
            obj,
            frames=8,
            cycles_samples=20,
            resolution_percentage=25,
        )
    elif args.turntable:
        turntable(bpy, root, obj)


if __name__ == "__main__":
    main()
