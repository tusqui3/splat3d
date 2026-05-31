
# INTEGRATION POINT — replace this stub with real Gaussian Splatting training.
#
# Option A — Nerfstudio (recommended, easiest setup):
#   pip install nerfstudio
#   ns-train splatfacto \
#       --data {colmap_dir} \
#       --output-dir {gs_dir} \
#       --max-num-iterations 7000
#
# Option B — Original 3DGS (graphdeco-inria):
#   git clone https://github.com/graphdeco-inria/gaussian-splatting
#   python train.py -s {colmap_dir} -m {gs_dir} --iterations 7000
#
# Option C — gsplat (fast, modern):
#   pip install gsplat
#   python -m gsplat.strategy.default --data_dir {colmap_dir} --result_dir {gs_dir}
#
# GPU requirement: NVIDIA GPU with CUDA 11.8+, 8GB+ VRAM for typical scenes.
# Training time: ~10 min (7k iters) to ~45 min (30k iters) on an RTX 3090.

import time
from pathlib import Path


def run_3dgs(colmap_dir: Path, gs_dir: Path):
    gs_dir.mkdir(parents=True, exist_ok=True)
    (gs_dir / "point_cloud").mkdir(parents=True, exist_ok=True)
    time.sleep(5)
    (gs_dir / "point_cloud" / "stub.txt").write_text("# 3DGS stub output\n")
