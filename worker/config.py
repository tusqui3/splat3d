import os
from pathlib import Path

DATA_DIR = Path(os.getenv("DATA_DIR", "/data"))
JOBS_DIR = DATA_DIR / "jobs"
DB_PATH = DATA_DIR / "jobs.db"
POLL_INTERVAL_SECONDS = float(os.getenv("POLL_INTERVAL_SECONDS", "2"))
FRAMES_PER_SECOND = int(os.getenv("FRAMES_PER_SECOND", "2"))
