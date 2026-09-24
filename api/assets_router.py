"""
Assets REST API Router for ViralStudio.
Handles asset uploading, registration, metadata extraction, and library listing.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from services.asset_service import AssetService
from models.domain import AssetModel

router = APIRouter(prefix="/api/assets", tags=["Assets"])

@router.post("/upload", response_model=AssetModel)
async def upload_asset(
    file: UploadFile = File(...),
    project_id: Optional[str] = Form(None),
    source: str = Form("upload"),
    provenance: Optional[str] = Form(None),
):
    """
    Uploads a local media asset (video, image, audio), calculates SHA256,
    extracts metadata via FFprobe, and registers it in the local asset library.
    """
    try:
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="Fail yang dimuat naik adalah kosong.")

        asset = AssetService.register_asset(
            file_bytes=content,
            filename=file.filename or "uploaded_media.mp4",
            project_id=project_id,
            source=source,
            provenance=provenance or f"Muat naik pengguna: {file.filename}",
        )
        return asset
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ralat semasa memproses aset: {str(e)}")

@router.get("", response_model=List[AssetModel])
async def list_assets(
    project_id: Optional[str] = None,
    type: Optional[str] = None,
):
    """Lists assets in the library with optional filters."""
    return AssetService.list_assets(project_id=project_id, asset_type=type)
