"""
Computer Use & Browser Use REST API Router.
Enables web navigation, action execution, autonomous task execution loops,
and screenshot streaming for ChatGPT Desktop / Claude Computer Use experiences.
"""

from typing import Dict, Any, Optional, List
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from services.computer_use_service import ComputerUseService, SCREENSHOTS_DIR

router = APIRouter(prefix="/api/browser", tags=["Computer Use"])


class NavigateRequest(BaseModel):
    url: str = Field(..., description="Target website URL")
    wait_seconds: Optional[int] = 2


class ActionRequest(BaseModel):
    action_type: str = Field(..., description="click, type, press, scroll, extract")
    selector: Optional[str] = ""
    text: Optional[str] = ""
    key: Optional[str] = ""
    scroll_y: Optional[int] = 300


class TaskRequest(BaseModel):
    goal: str = Field(..., description="High-level goal for autonomous agent to execute")
    max_steps: Optional[int] = 5


@router.get("/status")
async def get_browser_status():
    """Returns current browser engine status, active page, and latest screenshot."""
    return ComputerUseService.get_status()


@router.get("/history")
async def get_action_history():
    """Returns action audit history."""
    return ComputerUseService.get_history()


@router.post("/navigate")
async def navigate_browser(req: NavigateRequest):
    """Navigates to URL and takes screenshot."""
    try:
        return await ComputerUseService.navigate(req.url, req.wait_seconds or 2)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ralat navigasi pelayar: {e}")


@router.post("/action")
async def execute_browser_action(req: ActionRequest):
    """Executes a single browser action."""
    try:
        return await ComputerUseService.execute_action(
            action_type=req.action_type,
            selector=req.selector or "",
            text=req.text or "",
            key=req.key or "",
            scroll_y=req.scroll_y or 300
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ralat tindakan pelayar: {e}")


@router.post("/task")
async def run_autonomous_browser_task(req: TaskRequest):
    """
    Runs multi-step autonomous goal-directed browser use agent task
    (like ChatGPT Desktop and Claude Computer Use).
    """
    try:
        return await ComputerUseService.run_autonomous_task(req.goal, req.max_steps or 5)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ralat pelaksanaan tugasan berautonomi: {e}")


@router.get("/screenshot/{filename}")
async def get_screenshot_file(filename: str):
    """Returns the captured screenshot image."""
    file_path = SCREENSHOTS_DIR / filename
    if file_path.exists():
        media_type = "image/svg+xml" if filename.endswith(".svg") else "image/png"
        return FileResponse(str(file_path), media_type=media_type)
    raise HTTPException(status_code=404, detail="Tangkapan skrin tidak ditemui")
