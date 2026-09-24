"""
Jobs & Render Queue REST API Router for ViralStudio.
Provides endpoints for monitoring jobs, polling progress, requesting cancellation,
and initiating project-level vertical video renders.
"""

import sys
import asyncio
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks, Body
from services.job_service import JobService
from services.project_service import ProjectService
from services.tts_service import synthesize_speech
from services.renderer_service import render_vertical_video
from models.domain import JobModel

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])

async def execute_project_render_job(job_id: str, project_id: str, voice: str, bg_video: str):
    """Background worker executing speech synthesis and FFmpeg composition."""
    try:
        JobService.update_job_progress(job_id, 0.1, state="RUNNING")

        # Check cancellation
        if JobService.is_cancelled(job_id):
            JobService.update_job_progress(job_id, 0.0, state="CANCELLED")
            return

        proj = ProjectService.get_project(project_id)
        if not proj or not proj.scenes:
            JobService.fail_job(job_id, "NO_SCENES", "Projek tiada babak untuk dirender.")
            return

        # Combine scene scripts
        combined_script = " ".join(s.script.strip() for s in proj.scenes if s.script.strip())
        if not combined_script:
            JobService.fail_job(job_id, "EMPTY_SCRIPT", "Semua babak projek tidak mempunyai teks skrip.")
            return

        JobService.update_job_progress(job_id, 0.3)

        # 1. Synthesize Speech
        tts_res = await synthesize_speech(text=combined_script, voice=voice)
        audio_path = tts_res["audio_path"]

        if JobService.is_cancelled(job_id):
            JobService.update_job_progress(job_id, 0.0, state="CANCELLED")
            return

        JobService.update_job_progress(job_id, 0.6)

        # 2. Render Vertical Video in separate worker thread
        render_res = await asyncio.to_thread(
            render_vertical_video,
            audio_path,
            bg_video,
            combined_script
        )

        JobService.update_job_progress(job_id, 0.95)

        # Mark completed
        JobService.complete_job(job_id, output_ids=[render_res["video_url"]])

        # Update project status
        ProjectService.update_project(
            project_id,
            type("UpdateStub", (), {"title": None, "language": None, "brand_kit_id": None, "brief": None, "status": "COMPLETED", "version": proj.version})
        )

    except Exception as e:
        JobService.fail_job(job_id, "RENDER_ERROR", str(e))

@router.get("", response_model=List[JobModel])
async def list_jobs(project_id: Optional[str] = None, limit: int = 20):
    """Lists recent background jobs for the render queue view."""
    return JobService.list_jobs(project_id=project_id, limit=limit)

@router.get("/{job_id}", response_model=JobModel)
async def get_job(job_id: str):
    """Retrieves status and progress of a specific job."""
    job = JobService.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} tidak dijumpai.")
    return job

@router.post("/{job_id}/cancel")
async def cancel_job(job_id: str):
    """Requests cancellation of an ongoing or queued job."""
    success = JobService.request_cancellation(job_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Job {job_id} tidak dijumpai.")
    return {"status": "success", "message": f"Pembatalan job {job_id} telah diminta."}

@router.post("/render-project/{project_id}")
async def enqueue_project_render(
    project_id: str,
    background_tasks: BackgroundTasks,
    payload: dict = Body(default_factory=dict)
):
    """Enqueues a new asynchronous project render job."""
    proj = ProjectService.get_project(project_id)
    if not proj:
        raise HTTPException(status_code=404, detail=f"Projek {project_id} tidak dijumpai.")

    voice = payload.get("voice", "ms-MY-YasminNeural")
    bg_video = payload.get("bg_video", "dohnut-hands-making-donut.mp4")

    job = JobService.create_job(
        job_type="render_video",
        input_payload={"project_id": project_id, "voice": voice, "bg_video": bg_video},
        project_id=project_id
    )

    # Launch background task
    background_tasks.add_task(execute_project_render_job, job.id, project_id, voice, bg_video)

    return {
        "status": "queued",
        "job_id": job.id,
        "message": "Job render video telah dimasukkan ke dalam barisan (queue)."
    }
