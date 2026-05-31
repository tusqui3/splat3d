import logging
from fastapi import APIRouter
from database import fetch_all_jobs

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/admin/jobs")
async def list_jobs(limit: int = 100):
    jobs = await fetch_all_jobs(limit)
    logger.info("admin listed %d jobs", len(jobs))
    return jobs
