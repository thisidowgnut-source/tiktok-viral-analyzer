"""
Projects and Scenes REST API Router for ViralStudio.
Provides endpoints for creating, reading, updating, autosaving, deleting projects and scenes,
as well as exporting and importing project bundles.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Body
from services.project_service import ProjectService
from models.domain import (
    ProjectCreate,
    ProjectUpdate,
    ProjectSummary,
    ProjectDetail,
    SceneModel,
    SceneCreate,
)

router = APIRouter(prefix="/api/projects", tags=["Projects"])

@router.get("", response_model=List[ProjectSummary])
async def list_projects():
    """Lists all saved projects with summary metadata."""
    return ProjectService.list_projects()

@router.post("", response_model=ProjectDetail)
async def create_project(data: ProjectCreate):
    """Creates a new project in SQLite."""
    if not data.title.strip():
        raise HTTPException(status_code=400, detail="Tajuk projek wajib diisi.")
    return ProjectService.create_project(data)

@router.get("/{project_id}", response_model=ProjectDetail)
async def get_project(project_id: str):
    """Retrieves full project details including ordered scenes."""
    proj = ProjectService.get_project(project_id)
    if not proj:
        raise HTTPException(status_code=404, detail=f"Projek {project_id} tidak dijumpai.")
    return proj

@router.put("/{project_id}", response_model=ProjectDetail)
async def update_project(project_id: str, data: ProjectUpdate):
    """
    Updates project with optimistic locking version check.
    Returns 409 Conflict if client version does not match database version.
    """
    try:
        return ProjectService.update_project(project_id, data)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.delete("/{project_id}")
async def delete_project(project_id: str):
    """Deletes a project and its cascaded scenes."""
    success = ProjectService.delete_project(project_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Projek {project_id} tidak dijumpai.")
    return {"status": "success", "message": f"Projek {project_id} telah dipadam."}

@router.post("/{project_id}/scenes", response_model=SceneModel)
async def add_scene(project_id: str, scene: SceneCreate):
    """Appends a new scene to a project."""
    proj = ProjectService.get_project(project_id)
    if not proj:
        raise HTTPException(status_code=404, detail=f"Projek {project_id} tidak dijumpai.")
    return ProjectService.add_scene(project_id, scene)

@router.put("/scenes/{scene_id}", response_model=SceneModel)
async def update_scene(scene_id: str, updates: dict = Body(...)):
    """Updates a scene's properties (script, duration, asset, focal point, transition)."""
    updated = ProjectService.update_scene(scene_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Babak {scene_id} tidak dijumpai.")
    return updated

@router.delete("/scenes/{scene_id}")
async def delete_scene(scene_id: str):
    """Deletes a scene."""
    success = ProjectService.delete_scene(scene_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Babak {scene_id} tidak dijumpai.")
    return {"status": "success", "message": f"Babak {scene_id} telah dipadam."}

@router.get("/{project_id}/bundle")
async def export_bundle(project_id: str):
    """Exports a project and all its scenes as a portable JSON bundle."""
    try:
        return ProjectService.export_project_bundle(project_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/import/bundle", response_model=ProjectDetail)
async def import_bundle(bundle: dict = Body(...)):
    """Imports a project bundle into the local database with new unique IDs."""
    try:
        return ProjectService.import_project_bundle(bundle)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Gagal mengimport bundle projek: {str(e)}")
