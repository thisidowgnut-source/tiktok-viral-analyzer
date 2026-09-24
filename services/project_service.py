"""
Project Service for ViralStudio.
Handles persistence, CRUD, autosave with optimistic version control, scene management,
and project bundle export/import.
"""

import sys
import uuid
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Dict, Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from db.database import get_db
from models.domain import (
    ProjectCreate,
    ProjectUpdate,
    ProjectSummary,
    ProjectDetail,
    SceneModel,
    SceneCreate,
)

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

class ProjectService:
    @staticmethod
    def create_project(data: ProjectCreate) -> ProjectDetail:
        """Creates a new project in SQLite with default initial scene."""
        project_id = str(uuid.uuid4())
        now = _now_iso()
        brief_json = json.dumps(data.brief)

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO projects (id, title, language, brand_kit_id, brief, status, version, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, 'DRAFT', 1, ?, ?)
                """,
                (project_id, data.title, data.language, data.brand_kit_id, brief_json, now, now),
            )

            # Create default Hook scene (Phase 1)
            default_scene_id = str(uuid.uuid4())
            cursor.execute(
                """
                INSERT INTO scenes (id, project_id, sequence, script, duration, asset_id, crop_focal_point, transition, created_at, updated_at)
                VALUES (?, ?, 1, ?, 3.0, NULL, 'center', 'cut', ?, ?)
                """,
                (
                    default_scene_id,
                    project_id,
                    data.brief.get("hook_text", "Dengar bunyi krup-krap kerak doh panas ni..."),
                    now,
                    now,
                ),
            )

        return ProjectService.get_project(project_id)

    @staticmethod
    def get_project(project_id: str) -> Optional[ProjectDetail]:
        """Retrieves a project by ID with all scenes ordered by sequence."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, title, language, brand_kit_id, brief, status, version, created_at, updated_at FROM projects WHERE id = ?",
                (project_id,),
            )
            row = cursor.fetchone()
            if not row:
                return None

            brief_data = json.loads(row["brief"]) if row["brief"] else {}

            cursor.execute(
                """
                SELECT id, project_id, sequence, script, duration, asset_id, crop_focal_point, transition, created_at, updated_at
                FROM scenes WHERE project_id = ? ORDER BY sequence ASC
                """,
                (project_id,),
            )
            scene_rows = cursor.fetchall()

            scenes = [
                SceneModel(
                    id=s["id"],
                    project_id=s["project_id"],
                    sequence=s["sequence"],
                    script=s["script"],
                    duration=s["duration"],
                    asset_id=s["asset_id"],
                    crop_focal_point=s["crop_focal_point"],
                    transition=s["transition"],
                    created_at=s["created_at"],
                    updated_at=s["updated_at"],
                )
                for s in scene_rows
            ]

            return ProjectDetail(
                id=row["id"],
                title=row["title"],
                language=row["language"],
                brand_kit_id=row["brand_kit_id"],
                brief=brief_data,
                status=row["status"],
                version=row["version"],
                scenes=scenes,
                created_at=row["created_at"],
                updated_at=row["updated_at"],
            )

    @staticmethod
    def list_projects() -> List[ProjectSummary]:
        """Lists all projects with scene counts and total duration."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT p.id, p.title, p.language, p.brand_kit_id, p.status, p.version, p.created_at, p.updated_at,
                       COUNT(s.id) as scene_count,
                       COALESCE(SUM(s.duration), 0.0) as total_duration
                FROM projects p
                LEFT JOIN scenes s ON p.id = s.project_id
                GROUP BY p.id
                ORDER BY p.updated_at DESC
                """
            )
            rows = cursor.fetchall()
            return [
                ProjectSummary(
                    id=r["id"],
                    title=r["title"],
                    language=r["language"],
                    brand_kit_id=r["brand_kit_id"],
                    status=r["status"],
                    version=r["version"],
                    scene_count=r["scene_count"],
                    total_duration=round(r["total_duration"], 2),
                    created_at=r["created_at"],
                    updated_at=r["updated_at"],
                )
                for r in rows
            ]

    @staticmethod
    def update_project(project_id: str, data: ProjectUpdate) -> ProjectDetail:
        """
        Updates project with optimistic locking version check.
        Raises ValueError on version conflict.
        """
        now = _now_iso()
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT version FROM projects WHERE id = ?", (project_id,))
            row = cursor.fetchone()
            if not row:
                raise KeyError(f"Project {project_id} not found.")

            current_ver = row["version"]
            if current_ver != data.version:
                raise ValueError(
                    f"Version conflict: current database version is {current_ver}, but client sent {data.version}. Please reload project."
                )

            fields = []
            values = []

            if data.title is not None:
                fields.append("title = ?")
                values.append(data.title)
            if data.language is not None:
                fields.append("language = ?")
                values.append(data.language)
            if data.brand_kit_id is not None:
                fields.append("brand_kit_id = ?")
                values.append(data.brand_kit_id)
            if data.brief is not None:
                fields.append("brief = ?")
                values.append(json.dumps(data.brief))
            if data.status is not None:
                fields.append("status = ?")
                values.append(data.status)

            fields.append("version = version + 1")
            fields.append("updated_at = ?")
            values.append(now)

            values.append(project_id)
            values.append(current_ver)

            sql = f"UPDATE projects SET {', '.join(fields)} WHERE id = ? AND version = ?"
            cursor.execute(sql, values)

            if cursor.rowcount == 0:
                raise ValueError("Concurrent update prevented. Please reload project.")

        return ProjectService.get_project(project_id)

    @staticmethod
    def delete_project(project_id: str) -> bool:
        """Deletes a project and cascaded scenes."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
            return cursor.rowcount > 0

    @staticmethod
    def add_scene(project_id: str, scene: SceneCreate) -> SceneModel:
        """Appends a new scene to a project."""
        scene_id = str(uuid.uuid4())
        now = _now_iso()
        with get_db() as conn:
            cursor = conn.cursor()
            # Find next sequence
            cursor.execute("SELECT MAX(sequence) as max_seq FROM scenes WHERE project_id = ?", (project_id,))
            row = cursor.fetchone()
            next_seq = (row["max_seq"] or 0) + 1 if scene.sequence <= 0 else scene.sequence

            cursor.execute(
                """
                INSERT INTO scenes (id, project_id, sequence, script, duration, asset_id, crop_focal_point, transition, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    scene_id,
                    project_id,
                    next_seq,
                    scene.script,
                    scene.duration,
                    scene.asset_id,
                    scene.crop_focal_point,
                    scene.transition,
                    now,
                    now,
                ),
            )
            # Update project updated_at and increment version
            cursor.execute("UPDATE projects SET version = version + 1, updated_at = ? WHERE id = ?", (now, project_id))

        return SceneModel(
            id=scene_id,
            project_id=project_id,
            sequence=next_seq,
            script=scene.script,
            duration=scene.duration,
            asset_id=scene.asset_id,
            crop_focal_point=scene.crop_focal_point,
            transition=scene.transition,
            created_at=now,
            updated_at=now,
        )

    @staticmethod
    def update_scene(scene_id: str, updates: Dict[str, Any]) -> Optional[SceneModel]:
        """Updates a scene's properties."""
        now = _now_iso()
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, project_id FROM scenes WHERE id = ?", (scene_id,))
            row = cursor.fetchone()
            if not row:
                return None

            project_id = row["project_id"]
            fields = []
            values = []

            for key in ["sequence", "script", "duration", "asset_id", "crop_focal_point", "transition"]:
                if key in updates:
                    fields.append(f"{key} = ?")
                    values.append(updates[key])

            if not fields:
                return None

            fields.append("updated_at = ?")
            values.append(now)
            values.append(scene_id)

            cursor.execute(f"UPDATE scenes SET {', '.join(fields)} WHERE id = ?", values)
            cursor.execute("UPDATE projects SET version = version + 1, updated_at = ? WHERE id = ?", (now, project_id))

            cursor.execute(
                "SELECT id, project_id, sequence, script, duration, asset_id, crop_focal_point, transition, created_at, updated_at FROM scenes WHERE id = ?",
                (scene_id,),
            )
            s = cursor.fetchone()
            return SceneModel(
                id=s["id"],
                project_id=s["project_id"],
                sequence=s["sequence"],
                script=s["script"],
                duration=s["duration"],
                asset_id=s["asset_id"],
                crop_focal_point=s["crop_focal_point"],
                transition=s["transition"],
                created_at=s["created_at"],
                updated_at=s["updated_at"],
            )

    @staticmethod
    def delete_scene(scene_id: str) -> bool:
        """Deletes a scene and updates the project."""
        now = _now_iso()
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT project_id FROM scenes WHERE id = ?", (scene_id,))
            row = cursor.fetchone()
            if not row:
                return False

            project_id = row["project_id"]
            cursor.execute("DELETE FROM scenes WHERE id = ?", (scene_id,))
            cursor.execute("UPDATE projects SET version = version + 1, updated_at = ? WHERE id = ?", (now, project_id))
            return True

    @staticmethod
    def export_project_bundle(project_id: str) -> dict:
        """Exports a project and its scenes as a portable JSON bundle."""
        proj = ProjectService.get_project(project_id)
        if not proj:
            raise KeyError(f"Project {project_id} not found.")
        return {
            "format": "viralstudio_bundle_v1",
            "exported_at": _now_iso(),
            "project": proj.model_dump(),
        }

    @staticmethod
    def import_project_bundle(bundle: dict) -> ProjectDetail:
        """Imports a project bundle with new unique IDs to prevent collision."""
        if bundle.get("format") != "viralstudio_bundle_v1" or "project" not in bundle:
            raise ValueError("Invalid ViralStudio project bundle format.")

        p_data = bundle["project"]
        create_req = ProjectCreate(
            title=f"{p_data.get('title', 'Imported Project')} (Imported)",
            language=p_data.get("language", "ms"),
            brand_kit_id=p_data.get("brand_kit_id", "brand_dohnut_default"),
            brief=p_data.get("brief", {}),
        )
        new_project = ProjectService.create_project(create_req)

        # Clear default scene and add scenes from bundle
        with get_db() as conn:
            conn.execute("DELETE FROM scenes WHERE project_id = ?", (new_project.id,))

        for s in p_data.get("scenes", []):
            ProjectService.add_scene(
                new_project.id,
                SceneCreate(
                    sequence=s.get("sequence", 1),
                    script=s.get("script", ""),
                    duration=s.get("duration", 3.0),
                    asset_id=s.get("asset_id"),
                    crop_focal_point=s.get("crop_focal_point", "center"),
                    transition=s.get("transition", "cut"),
                ),
            )

        return ProjectService.get_project(new_project.id)
