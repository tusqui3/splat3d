import time
import sqlite3
import logging
from datetime import datetime, timezone
from pathlib import Path
from pipeline.extract_frames import extract_frames
from pipeline.run_colmap import run_colmap
from pipeline.run_3dgs import run_3dgs
from pipeline.export import export_splat
from config import DB_PATH, JOBS_DIR, POLL_INTERVAL_SECONDS, DATA_DIR

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def db_connect() -> sqlite3.Connection:
    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row
    return db


def update_job(db: sqlite3.Connection, job_id: str, status: str, progress: int = 0,
               error: str | None = None, result_path: str | None = None):
    if error:
        db.execute(
            "UPDATE jobs SET status=?, updated_at=?, error_message=?, progress=? WHERE id=?",
            (status, now_iso(), error, progress, job_id),
        )
    elif result_path:
        db.execute(
            "UPDATE jobs SET status=?, updated_at=?, result_path=?, progress=? WHERE id=?",
            (status, now_iso(), result_path, progress, job_id),
        )
    else:
        db.execute(
            "UPDATE jobs SET status=?, updated_at=?, progress=? WHERE id=?",
            (status, now_iso(), progress, job_id),
        )
    db.commit()


def process_job(job_id: str, video_path: Path):
    job_dir = JOBS_DIR / job_id
    db = db_connect()
    try:
        logger.info("[%s] starting pipeline", job_id)

        update_job(db, job_id, "extracting_frames", 10)
        frames_dir = job_dir / "frames"
        extract_frames(video_path, frames_dir)
        logger.info("[%s] frames extracted", job_id)

        update_job(db, job_id, "running_colmap", 30)
        colmap_dir = job_dir / "colmap"
        run_colmap(frames_dir, colmap_dir)
        logger.info("[%s] colmap done", job_id)

        update_job(db, job_id, "running_3dgs", 55)
        gs_dir = job_dir / "3dgs"
        run_3dgs(colmap_dir, gs_dir)
        logger.info("[%s] 3dgs training done", job_id)

        update_job(db, job_id, "exporting", 90)
        output_path = job_dir / "output.splat"
        export_splat(gs_dir, output_path)
        logger.info("[%s] export done path=%s", job_id, output_path)

        update_job(db, job_id, "done", 100, result_path=str(output_path))
        logger.info("[%s] complete", job_id)

    except Exception as exc:
        logger.error("[%s] failed: %s", job_id, exc, exc_info=True)
        update_job(db, job_id, "failed", error=str(exc))
    finally:
        db.close()


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    logger.info("worker started, polling every %.1fs", POLL_INTERVAL_SECONDS)

    while True:
        db = None
        try:
            db = db_connect()
            row = db.execute(
                "SELECT * FROM jobs WHERE status='pending' ORDER BY created_at ASC LIMIT 1"
            ).fetchone()

            if row:
                job = dict(row)
                db.execute(
                    "UPDATE jobs SET status='processing', updated_at=? WHERE id=?",
                    (now_iso(), job["id"]),
                )
                db.commit()
                db.close()
                db = None
                process_job(job["id"], Path(job["video_path"]))
            else:
                db.close()
                db = None
                time.sleep(POLL_INTERVAL_SECONDS)

        except Exception as exc:
            logger.error("worker loop error: %s", exc, exc_info=True)
            if db:
                try:
                    db.close()
                except Exception:
                    pass
            time.sleep(5)


if __name__ == "__main__":
    main()
