"""
Job Queue and Execution Service for ViralStudio.
Provides SQLite-backed state tracking, progress monitoring, cancellation support,
and ThreadPool worker dispatch.
"""

import sys
import uuid
import json
import concurrent.futures
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any, Callable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from db.database import get_db
from models.domain import JobModel

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

# Bounded worker pool for CPU/FFmpeg heavy operations
_EXECUTOR = concurrent.futures.ThreadPoolExecutor(max_workers=2, thread_name_prefix="ViralStudioWorker")

class JobService:
    @staticmethod
    def create_job(job_type: str, input_payload: Dict[str, Any], project_id: Optional[str] = None) -> JobModel:
        """Enqueues a new background job."""
        job_id = str(uuid.uuid4())
        now = _now_iso()
        input_hash = json.dumps(input_payload, sort_keys=True)

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO jobs (id, project_id, type, input_hash, state, progress, attempts, output_ids, cancellation_requested, created_at, updated_at)
                VALUES (?, ?, ?, ?, 'QUEUED', 0.0, 0, '[]', 0, ?, ?)
                """,
                (job_id, project_id, job_type, input_hash, now, now),
            )

        return JobService.get_job(job_id)

    @staticmethod
    def get_job(job_id: str) -> Optional[JobModel]:
        """Fetches current job status and progress."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return JobModel(
                id=row["id"],
                project_id=row["project_id"],
                type=row["type"],
                input_hash=row["input_hash"],
                state=row["state"],
                progress=row["progress"],
                error_code=row["error_code"],
                error_message=row["error_message"],
                attempts=row["attempts"],
                output_ids=json.loads(row["output_ids"]) if row["output_ids"] else [],
                cancellation_requested=bool(row["cancellation_requested"]),
                created_at=row["created_at"],
                updated_at=row["updated_at"],
            )

    @staticmethod
    def update_job_progress(job_id: str, progress: float, state: Optional[str] = None):
        """Updates progress and optional state."""
        now = _now_iso()
        with get_db() as conn:
            cursor = conn.cursor()
            if state:
                cursor.execute(
                    "UPDATE jobs SET progress = ?, state = ?, updated_at = ? WHERE id = ?",
                    (progress, state, now, job_id),
                )
            else:
                cursor.execute(
                    "UPDATE jobs SET progress = ?, updated_at = ? WHERE id = ?",
                    (progress, now, job_id),
                )

    @staticmethod
    def complete_job(job_id: str, output_ids: List[str]):
        """Marks job as COMPLETED with output asset references."""
        now = _now_iso()
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE jobs
                SET state = 'COMPLETED', progress = 1.0, output_ids = ?, updated_at = ?
                WHERE id = ?
                """,
                (json.dumps(output_ids), now, job_id),
            )

    @staticmethod
    def fail_job(job_id: str, error_code: str, error_message: str):
        """Marks job as FAILED with actionable error information."""
        now = _now_iso()
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE jobs
                SET state = 'FAILED', error_code = ?, error_message = ?, updated_at = ?
                WHERE id = ?
                """,
                (error_code, error_message, now, job_id),
            )

    @staticmethod
    def request_cancellation(job_id: str) -> bool:
        """Requests cancellation of an ongoing or queued job."""
        now = _now_iso()
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE jobs SET cancellation_requested = 1, updated_at = ? WHERE id = ?",
                (now, job_id),
            )
            return cursor.rowcount > 0

    @staticmethod
    def is_cancelled(job_id: str) -> bool:
        """Checks if job cancellation has been requested."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT cancellation_requested FROM jobs WHERE id = ?", (job_id,))
            row = cursor.fetchone()
            return bool(row["cancellation_requested"]) if row else False

    @staticmethod
    def submit_task(fn: Callable, *args, **kwargs):
        """Dispatches a task to the background thread pool."""
        return _EXECUTOR.submit(fn, *args, **kwargs)

    @staticmethod
    def list_jobs(project_id: Optional[str] = None, limit: int = 20) -> List[JobModel]:
        """Lists recent jobs for the queue view."""
        with get_db() as conn:
            cursor = conn.cursor()
            if project_id:
                cursor.execute(
                    "SELECT * FROM jobs WHERE project_id = ? ORDER BY created_at DESC LIMIT ?",
                    (project_id, limit),
                )
            else:
                cursor.execute(
                    "SELECT * FROM jobs ORDER BY created_at DESC LIMIT ?",
                    (limit,),
                )
            rows = cursor.fetchall()
            return [
                JobModel(
                    id=r["id"],
                    project_id=r["project_id"],
                    type=r["type"],
                    input_hash=r["input_hash"],
                    state=r["state"],
                    progress=r["progress"],
                    error_code=r["error_code"],
                    error_message=r["error_message"],
                    attempts=r["attempts"],
                    output_ids=json.loads(r["output_ids"]) if r["output_ids"] else [],
                    cancellation_requested=bool(r["cancellation_requested"]),
                    created_at=r["created_at"],
                    updated_at=r["updated_at"],
                )
                for r in rows
            ]
