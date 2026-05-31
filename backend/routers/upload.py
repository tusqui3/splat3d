import uuid
import logging
from datetime import datetime, timezone
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from database import insert_job
from config import JOBS_DIR, ALLOWED_EXTENSIONS, MAX_VIDEO_SIZE_MB

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    ext = Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"Unsupported format. Allowed: {sorted(ALLOWED_EXTENSIONS)}")

    job_id = str(uuid.uuid4())
    job_dir = JOBS_DIR / job_id
    job_dir.mkdir(parents=True)
    video_path = job_dir / f"video{ext}"

    size = 0
    max_bytes = MAX_VIDEO_SIZE_MB * 1024 * 1024
    try:
        with open(video_path, "wb") as f:
            while chunk := await file.read(1024 * 1024):
                size += len(chunk)
                if size > max_bytes:
                    raise HTTPException(413, f"File exceeds {MAX_VIDEO_SIZE_MB}MB limit")
                f.write(chunk)
    except HTTPException:
        if video_path.exists():
            video_path.unlink()
        raise

    now = datetime.now(timezone.utc).isoformat()
    await insert_job(job_id, str(video_path), now)
    logger.info("job created job_id=%s size_bytes=%d", job_id, size)

    return {"job_id": job_id}
