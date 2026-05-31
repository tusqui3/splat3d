import aiosqlite
from config import DB_PATH, DATA_DIR

DATA_DIR.mkdir(parents=True, exist_ok=True)


async def init_db():
    async with aiosqlite.connect(str(DB_PATH)) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                video_path TEXT,
                result_path TEXT,
                error_message TEXT,
                progress INTEGER DEFAULT 0
            )
        """)
        await db.commit()


async def fetch_job(job_id: str):
    async with aiosqlite.connect(str(DB_PATH)) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)) as cur:
            row = await cur.fetchone()
    return dict(row) if row else None


async def fetch_all_jobs(limit: int = 100):
    async with aiosqlite.connect(str(DB_PATH)) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM jobs ORDER BY created_at DESC LIMIT ?", (limit,)
        ) as cur:
            rows = await cur.fetchall()
    return [dict(r) for r in rows]


async def insert_job(job_id: str, video_path: str, now: str):
    async with aiosqlite.connect(str(DB_PATH)) as db:
        await db.execute(
            "INSERT INTO jobs (id, status, created_at, updated_at, video_path) VALUES (?, 'pending', ?, ?, ?)",
            (job_id, now, now, video_path),
        )
        await db.commit()
