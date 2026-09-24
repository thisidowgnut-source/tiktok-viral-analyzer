"""
MCP (Model Context Protocol) REST API Router.
Enables listing connected MCP servers, tool discovery, schema inspection, and tool testing.
"""

from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from services.mcp_service import MCPService

router = APIRouter(prefix="/api/mcp", tags=["MCP Servers"])


class CallToolRequest(BaseModel):
    server_id: str
    tool_name: str
    arguments: Dict[str, Any] = {}


class AddServerRequest(BaseModel):
    name: str
    transport: str = "stdio"
    url_or_cmd: str
    description: Optional[str] = ""


@router.get("/servers")
async def get_mcp_servers():
    """Returns connected MCP servers with status, latency, and tools."""
    return MCPService.list_servers()


@router.get("/tools")
async def get_all_mcp_tools():
    """Returns all available MCP tools across all connected servers."""
    return MCPService.list_all_tools()


@router.post("/call")
async def call_mcp_tool_endpoint(req: CallToolRequest):
    """Executes an MCP tool and returns output and calibrated execution latency."""
    try:
        return MCPService.call_tool(req.server_id, req.tool_name, req.arguments)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ralat panggilan MCP Tool: {e}")


@router.post("/servers/add")
async def add_mcp_server_endpoint(req: AddServerRequest):
    """Adds a new custom MCP server."""
    try:
        return MCPService.add_server(req.name, req.transport, req.url_or_cmd, req.description or "")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
