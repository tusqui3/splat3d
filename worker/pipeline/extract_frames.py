import subprocess
from pathlib import Path
from config import FRAMES_PER_SECOND


def extract_frames(video_path: Path, frames_dir: Path):
    frames_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", str(video_path),
            "-vf", f"fps={FRAMES_PER_SECOND}",
            "-q:v", "1",
            str(frames_dir / "%04d.jpg"),
        ],
        check=True,
        capture_output=True,
    )
