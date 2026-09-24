"""
Domain Pydantic V2 schemas for ViralStudio.
Provides strict contracts for Projects, Scenes, Assets, Jobs, and Brand Kits.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class BrandKitModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    name: str
    colors: Dict[str, str]
    logo_font: Dict[str, str]
    language_style: str
    cta: str
    product_facts: List[Dict[str, Any]]
    is_default: bool = False
    created_at: str
    updated_at: str

class SceneModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    project_id: str
    sequence: int
    script: str
    duration: float = 3.0
    asset_id: Optional[str] = None
    crop_focal_point: str = "center"
    transition: str = "cut"
    created_at: str
    updated_at: str

class SceneCreate(BaseModel):
    sequence: int = 1
    script: str
    duration: float = 3.0
    asset_id: Optional[str] = None
    crop_focal_point: str = "center"
    transition: str = "cut"

class AssetModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    project_id: Optional[str] = None
    type: str  # 'video', 'image', 'audio'
    source: str  # 'upload', 'generated', 'demo'
    internal_path: str
    filename: str
    checksum_sha256: str
    dimensions: Optional[str] = None
    duration: float = 0.0
    provenance: Optional[str] = None
    review_status: str = "UNREVIEWED"
    created_at: str

class JobModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    project_id: Optional[str] = None
    type: str  # 'render_video', 'tts', 'analysis'
    input_hash: str
    state: str = "QUEUED"  # 'QUEUED', 'RUNNING', 'COMPLETED', 'FAILED', 'CANCELLED'
    progress: float = 0.0
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    attempts: int = 0
    output_ids: List[str] = []
    cancellation_requested: bool = False
    created_at: str
    updated_at: str

class ProjectCreate(BaseModel):
    title: str
    language: str = "ms"
    brand_kit_id: Optional[str] = "brand_dohnut_default"
    brief: Dict[str, Any] = Field(default_factory=dict)

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    language: Optional[str] = None
    brand_kit_id: Optional[str] = None
    brief: Optional[Dict[str, Any]] = None
    status: Optional[str] = None
    version: int  # Required for optimistic concurrency control

class ProjectSummary(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    title: str
    language: str
    brand_kit_id: Optional[str]
    status: str
    version: int
    scene_count: int = 0
    total_duration: float = 0.0
    created_at: str
    updated_at: str

class ProjectDetail(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    title: str
    language: str
    brand_kit_id: Optional[str]
    brief: Dict[str, Any]
    status: str
    version: int
    scenes: List[SceneModel] = []
    created_at: str
    updated_at: str
