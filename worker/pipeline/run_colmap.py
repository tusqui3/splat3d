
# INTEGRATION POINT — replace this stub with real COLMAP execution.
#
# Real commands (requires `colmap` in PATH or Docker image):
#
#   colmap feature_extractor \
#       --database_path {colmap_dir}/database.db \
#       --image_path {frames_dir}
#
#   colmap exhaustive_matcher \
#       --database_path {colmap_dir}/database.db
#
#   colmap mapper \
#       --database_path {colmap_dir}/database.db \
#       --image_path {frames_dir} \
#       --output_path {colmap_dir}/sparse
#
#   colmap model_converter \
#       --input_path {colmap_dir}/sparse/0 \
#       --output_path {colmap_dir}/sparse/0 \
#       --output_type TXT
#
# For nerfstudio, use ns-process-data instead:
#   ns-process-data video --data {video_path} --output-dir {colmap_dir}

import time
from pathlib import Path


def run_colmap(frames_dir: Path, colmap_dir: Path):
    colmap_dir.mkdir(parents=True, exist_ok=True)
    (colmap_dir / "sparse").mkdir(parents=True, exist_ok=True)
    time.sleep(3)
    (colmap_dir / "sparse" / "cameras.txt").write_text("# stub\n")
    (colmap_dir / "sparse" / "images.txt").write_text("# stub\n")
    (colmap_dir / "sparse" / "points3D.txt").write_text("# stub\n")
