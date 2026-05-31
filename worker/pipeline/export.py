
# INTEGRATION POINT — replace stub with real .splat export.
#
# After training, the model produces a .ply file at:
#   {gs_dir}/point_cloud/iteration_7000/point_cloud.ply  (3DGS / gsplat)
#   or nerfstudio exports via: ns-export gaussian-splats --load-config ...
#
# Convert .ply → .splat (antimatter15 binary format) using:
#   pip install plyfile
#   Then read SH coefficients + covariances and pack into .splat binary:
#     xyz: 3×f32, scale: 3×f32, color+opacity: 4×u8, rotation: 4×u8
#     = 32 bytes per Gaussian.
#
# Reference converter:
#   https://github.com/antimatter15/splat/blob/main/convert.py

import struct
import random
from pathlib import Path


def export_splat(gs_dir: Path, output_path: Path):
    gaussians = _generate_demo_cloud(count=4000)
    with open(output_path, "wb") as f:
        for g in gaussians:
            f.write(struct.pack("<ffffffBBBBBBBB", *g))


def _generate_demo_cloud(count: int):
    rng = random.Random(42)
    points = []
    for _ in range(count):
        x = rng.gauss(0, 0.5)
        y = rng.gauss(0, 0.3)
        z = rng.gauss(0, 0.5)
        sx = sy = sz = rng.uniform(0.008, 0.035)
        r = rng.randint(80, 230)
        g = rng.randint(60, 180)
        b = rng.randint(40, 130)
        a = rng.randint(160, 255)
        rw, rx, ry, rz = 128, 0, 0, 0
        points.append((x, y, z, sx, sy, sz, r, g, b, a, rw, rx, ry, rz))
    return points
