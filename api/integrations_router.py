"""
API Router for TypeSafe Jev System One & Google AI Studio integrations.
Adheres to Prompt G7 & Prompt G8 specifications.
"""

from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from services.jev_service import JevService
from services.google_adapter import GoogleAIStudioAdapter

router = APIRouter(prefix="/api/integrations", tags=["integrations"])


class JevRouteRequest(BaseModel):
    brief_text: str = Field(..., min_length=3, description="Campaign brief or prompt")


class JevBriefStatusRequest(BaseModel):
    brief_text: str = Field(..., min_length=3, description="Campaign brief")


class JevQualityRequest(BaseModel):
    script_text: str = Field(..., min_length=5, description="Full script text")
    product_facts: Optional[Dict[str, Any]] = None


class JevRevisionRequest(BaseModel):
    quality_score: float = Field(..., ge=1.0, le=10.0)
    issues_count: int = Field(default=0, ge=0)


class GooglePlanRequest(BaseModel):
    product_name: str = Field(default="Doh-Nut Nutella Lava", description="Product name")
    angle: str = Field(default="ASMR Craving", description="Marketing angle")
    target_duration: int = Field(default=15, ge=5, le=60)
    brand_tone: str = Field(default="Energetic, authentic Malaysian youth tone")


@router.post("/jev/route")
async def jev_route_endpoint(req: JevRouteRequest):
    """Classifies next workflow step (Prompt G8)."""
    return JevService.classify_route(req.brief_text)


@router.post("/jev/brief-status")
async def jev_brief_status_endpoint(req: JevBriefStatusRequest):
    """Checks whether brief has sufficient facts or missing requirements (Prompt G8)."""
    return JevService.evaluate_brief_status(req.brief_text)


@router.post("/jev/quality")
async def jev_quality_endpoint(req: JevQualityRequest):
    """Evaluates script on 4-axis rubric without speculative views forecasting (Prompt G8)."""
    return JevService.evaluate_script_quality(req.script_text, req.product_facts)


@router.post("/jev/revision")
async def jev_revision_endpoint(req: JevRevisionRequest):
    """Routes to accept_for_preview, revise_once, or request_missing_input (Prompt G8)."""
    return JevService.evaluate_revision_action(req.quality_score, req.issues_count)


@router.post("/google/plan")
async def google_plan_endpoint(req: GooglePlanRequest):
    """
    Generates structured scene plans using Google Gemini models with offline fallback (Prompt G7).
    """
    adapter = GoogleAIStudioAdapter()
    res = adapter.generate_scene_plan(
        product_name=req.product_name,
        angle=req.angle,
        target_duration=req.target_duration,
        brand_tone=req.brand_tone
    )
    return res.model_dump()


@router.get("/google/status")
async def google_status_endpoint():
    """Checks Google GenAI client configuration status and environment keys."""
    adapter = GoogleAIStudioAdapter()
    return {
        "configured": adapter.is_configured(),
        "model": adapter.model_name,
        "sdk_available": adapter.client is not None,
        "note": "Ready for live Gemini generation" if adapter.is_configured() else "Using local ground-truth fallback (No API key set in env)"
    }
