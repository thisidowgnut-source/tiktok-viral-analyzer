"""
Centralized Configuration for ViralStudio KA-363.
Supports relative path defaults with environment variable overrides, eliminating hardcoded machine paths.
"""

import os
from pathlib import Path

# Base project directory
BASE_DIR = Path(os.getenv("VIRALSTUDIO_BASE_DIR", Path(__file__).resolve().parent.parent))

IS_VERCEL = bool(os.getenv("VERCEL"))

if IS_VERCEL:
    DATA_DIR = Path("/tmp/data")
    DB_PATH = Path(os.getenv("VIRALSTUDIO_DB_PATH", DATA_DIR / "viralstudio.db"))
    STATIC_DIR = BASE_DIR / "static"
    EXPORTS_DIR = Path("/tmp/exports")
    UPLOADS_DIR = Path("/tmp/uploads")
else:
    DATA_DIR = BASE_DIR / "data"
    DB_PATH = Path(os.getenv("VIRALSTUDIO_DB_PATH", DATA_DIR / "viralstudio.db"))
    STATIC_DIR = BASE_DIR / "static"
    EXPORTS_DIR = STATIC_DIR / "exports"
    UPLOADS_DIR = STATIC_DIR / "uploads"

for d in (DATA_DIR, EXPORTS_DIR, UPLOADS_DIR):
    try:
        d.mkdir(parents=True, exist_ok=True)
    except OSError:
        pass

# Sibling projects with graceful relative resolution
DOHNUT_PUBLIC_DIR = Path(
    os.getenv("DOHNUT_PUBLIC_DIR", BASE_DIR.parent / "Doh-Nut" / "public")
)

JEV_PROJECT_DIR = Path(
    os.getenv("TYPESAFE_JEV_DIR", BASE_DIR.parent / "typesafe-system-one")
)

# Dataset path
DATASET_363_PATH = BASE_DIR / "khairulaming_all_363_analysis.json"

# Server configuration
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8765"))

# Security and timeouts
FFMPEG_TIMEOUT_SECONDS = int(os.getenv("FFMPEG_TIMEOUT_SECONDS", "180"))
MAX_SCRIPT_LENGTH = int(os.getenv("MAX_SCRIPT_LENGTH", "5000"))
ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv", ".webm"}
ALLOWED_AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".aac"}
ALLOWED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
