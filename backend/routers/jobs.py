from fastapi import APIRouter, HTTPException
from database import fetch_job

router = APIRouter()


@router.get("/jobs/{job_id}")
async def get_job(job_id: str):
    job = await fetch_job(job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    return job


@router.get("/jobs/{job_id}/result")
async def get_job_result(job_id: str):
    job = await fetch_job(job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    if job["status"] != "done":
        raise HTTPException(400, f"Job not complete — status: {job['status']}")
    return {
        "job_id": job_id,
        "splat_url": f"/data/jobs/{job_id}/output.splat",
    }
