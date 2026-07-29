from fastapi.responses import FileResponse
from app.downloader import download_video
from app.models import DownloadRequest
import os
from app.models import VideoRequest
from app.downloader import get_video_info
from fastapi import HTTPException
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import BackgroundTasks
from app.jobs import create_job, get_job
from app.worker import process_download

app = FastAPI(
    title="Video Downloader API",
    version="1.0.0"
)

# Allow Blogger (we'll tighten this later if desired)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/download")
async def download(
    request: DownloadRequest,
    background_tasks: BackgroundTasks
):

    job_id = create_job()

    background_tasks.add_task(
        process_download,
        job_id,
        request.url,
        request.format_id
    )

    return {
        "job_id": job_id
    }

@app.get("/api/status/{job_id}")
async def status(job_id: str):

    job = get_job(job_id)

    if not job:
        raise HTTPException(404, "Job not found")

    return job

@app.get("/")
async def home():
    return {
        "success": True,
        "message": "Video Downloader API is running"
    }

@app.get("/health")
@app.post("/api/info")
async def video_info(request: VideoRequest):

    try:
        return get_video_info(request.url)

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
async def health():
    return {
        "status": "ok"
    }