"""
Asset Service for ViralStudio.
Handles asset registration, SHA256 hashing, FFprobe metadata extraction,
and safe path traversal prevention.
"""

import sys
import uuid
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app_core.config import (
    UPLOADS_DIR,
    ALLOWED_VIDEO_EXTENSIONS,
    ALLOWED_AUDIO_EXTENSIONS,
    ALLOWED_IMAGE_EXTENSIONS,
)
from db.database import get_db
from models.domain import AssetModel

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def calculate_sha256(file_path: Path) -> str:
    """Calculates SHA256 hash of a file."""
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def probe_media_file(file_path: Path) -> Dict[str, Any]:
    """Runs ffprobe to safely extract dimensions and duration."""
    meta = {"dimensions": None, "duration": 0.0}
    try:
        cmd = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "stream=width,height,duration:format=duration",
            "-of", "json",
            str(file_path)
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if res.returncode == 0:
            data = json.loads(res.stdout)
            # Find duration
            if "format" in data and "duration" in data["format"]:
                meta["duration"] = float(data["format"]["duration"])
            # Find dimensions
            for stream in data.get("streams", []):
                if "width" in stream and "height" in stream:
                    meta["dimensions"] = f"{stream['width']}x{stream['height']}"
                    break
    except Exception as e:
        print(f"[!] Warning: ffprobe failed for {file_path.name}: {e}")
    return meta

class AssetService:
    @staticmethod
    def register_asset(
        file_bytes: bytes,
        filename: str,
        project_id: Optional[str] = None,
        source: str = "upload",
        provenance: Optional[str] = None,
    ) -> AssetModel:
        """Saves file bytes safely, extracts metadata, and records in SQLite."""
        safe_name = Path(filename).name.replace(" ", "_")
        ext = Path(safe_name).suffix.lower()

        # Determine asset type
        if ext in ALLOWED_VIDEO_EXTENSIONS:
            asset_type = "video"
        elif ext in ALLOWED_AUDIO_EXTENSIONS:
            asset_type = "audio"
        elif ext in ALLOWED_IMAGE_EXTENSIONS:
            asset_type = "image"
        else:
            raise ValueError(f"Disallowed file extension: {ext}")

        asset_id = str(uuid.uuid4())
        # Store with asset_id prefix to prevent filename collision
        stored_filename = f"{asset_id[:8]}_{safe_name}"
        dest_path = UPLOADS_DIR / stored_filename

        with open(dest_path, "wb") as f:
            f.write(file_bytes)

        checksum = calculate_sha256(dest_path)
        meta = probe_media_file(dest_path)
        now = _now_iso()
        internal_path = f"/static/uploads/{stored_filename}"

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO assets (id, project_id, type, source, internal_path, filename, checksum_sha256, dimensions, duration, provenance, review_status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'UNREVIEWED', ?)
                """,
                (
                    asset_id,
                    project_id,
                    asset_type,
                    source,
                    internal_path,
                    safe_name,
                    checksum,
                    meta["dimensions"],
                    meta["duration"],
                    provenance or f"User upload: {safe_name}",
                    now,
                ),
            )

        return AssetModel(
            id=asset_id,
            project_id=project_id,
            type=asset_type,
            source=source,
            internal_path=internal_path,
            filename=safe_name,
            checksum_sha256=checksum,
            dimensions=meta["dimensions"],
            duration=meta["duration"],
            provenance=provenance,
            review_status="UNREVIEWED",
            created_at=now,
        )

    @staticmethod
    def get_asset(asset_id: str) -> Optional[AssetModel]:
        """Retrieves asset metadata by ID."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM assets WHERE id = ?", (asset_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return AssetModel(
                id=row["id"],
                project_id=row["project_id"],
                type=row["type"],
                source=row["source"],
                internal_path=row["internal_path"],
                filename=row["filename"],
                checksum_sha256=row["checksum_sha256"],
                dimensions=row["dimensions"],
                duration=row["duration"],
                provenance=row["provenance"],
                review_status=row["review_status"],
                created_at=row["created_at"],
            )

    @staticmethod
    def list_assets(project_id: Optional[str] = None, asset_type: Optional[str] = None) -> List[AssetModel]:
        """Lists assets with optional project or type filtering."""
        with get_db() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM assets WHERE 1=1"
            params = []
            if project_id:
                query += " AND (project_id = ? OR project_id IS NULL)"
                params.append(project_id)
            if asset_type:
                query += " AND type = ?"
                params.append(asset_type)
            query += " ORDER BY created_at DESC"
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [
                AssetModel(
                    id=r["id"],
                    project_id=r["project_id"],
                    type=r["type"],
                    source=r["source"],
                    internal_path=r["internal_path"],
                    filename=r["filename"],
                    checksum_sha256=r["checksum_sha256"],
                    dimensions=r["dimensions"],
                    duration=r["duration"],
                    provenance=r["provenance"],
                    review_status=r["review_status"],
                    created_at=r["created_at"],
                )
                for r in rows
            ]
