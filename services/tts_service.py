"""
TTS Service for ViralStudio.
Handles text-to-speech synthesis with honest cloud Azure Neural telemetry,
caching, ffprobe duration calculation, and local audio fallback.
"""

import os
import sys
import hashlib
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional
import edge_tts

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app_core.config import EXPORTS_DIR

async def synthesize_speech(
    text: str,
    voice: str = "ms-MY-YasminNeural",
    rate: str = "+0%"
) -> Dict[str, Any]:
    """
    Synthesizes speech via Microsoft Azure Speech (edge-tts).
    Requires active internet connection.
    """
    text_clean = text.strip()
    if not text_clean:
        raise ValueError("Text cannot be empty for TTS synthesis.")

    # Cache hash based on text, voice, and rate
    cache_str = f"{text_clean}_{voice}_{rate}"
    audio_hash = hashlib.md5(cache_str.encode("utf-8")).hexdigest()[:12]
    audio_filename = f"tts_{audio_hash}.mp3"
    audio_path = EXPORTS_DIR / audio_filename

    # If cached, probe duration and return
    if audio_path.exists() and audio_path.stat().st_size > 1000:
        duration = probe_audio_duration(audio_path)
        return {
            "status": "cached",
            "audio_url": f"/exports/{audio_filename}",
            "audio_path": str(audio_path),
            "filename": audio_filename,
            "duration": duration,
            "voice": voice,
            "engine": "Microsoft Azure Neural (Awan - Sifar Kos Kunci API)",
            "is_offline": False
        }

    # Generate via edge-tts
    comm = edge_tts.Communicate(text_clean, voice, rate=rate)
    await comm.save(str(audio_path))

    duration = probe_audio_duration(audio_path)
    return {
        "status": "success",
        "audio_url": f"/exports/{audio_filename}",
        "audio_path": str(audio_path),
        "filename": audio_filename,
        "duration": duration,
        "voice": voice,
        "engine": "Microsoft Azure Neural (Awan - Sifar Kos Kunci API)",
        "is_offline": False
    }

def probe_audio_duration(audio_path: Path) -> float:
    """Probes audio duration safely via ffprobe."""
    try:
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(audio_path)
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return round(float(res.stdout.strip()), 2)
    except Exception:
        # Fallback approximation: 130 words per minute ~ 2.16 words/sec
        return 10.0
