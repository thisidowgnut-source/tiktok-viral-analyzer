"""
Marketplace & Plugins REST API Router.
Enables browsing, installing, configuring, and executing ChatGPT/Claude-style plugins.
"""

from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from services.marketplace_service import MarketplaceService

router = APIRouter(prefix="/api/plugins", tags=["Plugins & Marketplace"])


class TogglePluginRequest(BaseModel):
    plugin_id: str


class ConfigurePluginRequest(BaseModel):
    config: Dict[str, Any]


class RunPluginRequest(BaseModel):
    action: Optional[str] = "execute"
    params: Optional[Dict[str, Any]] = {}


@router.get("")
async def get_plugins(category: Optional[str] = None):
    """Returns list of all marketplace plugins."""
    return MarketplaceService.list_plugins(category)


@router.post("/{plugin_id}/toggle")
async def toggle_plugin_endpoint(plugin_id: str):
    """Installs or toggles active state of a plugin."""
    try:
        return MarketplaceService.toggle_plugin(plugin_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{plugin_id}/uninstall")
async def uninstall_plugin_endpoint(plugin_id: str):
    """Uninstalls a plugin."""
    try:
        return MarketplaceService.uninstall_plugin(plugin_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{plugin_id}/configure")
async def configure_plugin_endpoint(plugin_id: str, req: ConfigurePluginRequest):
    """Updates plugin configuration (API keys, preferences)."""
    try:
        return MarketplaceService.configure_plugin(plugin_id, req.config)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{plugin_id}/run")
async def run_plugin_endpoint(plugin_id: str, req: RunPluginRequest):
    """Executes a live capability of the plugin."""
    try:
        return MarketplaceService.execute_plugin(plugin_id, req.action or "execute", req.params or {})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
