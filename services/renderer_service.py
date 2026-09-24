"""
Renderer Service for ViralStudio.
Handles FFmpeg 9:16 vertical video composition, SRT kinetic subtitle creation,
atomic file writes (.tmp -> .mp4), timeout enforcement, and safe path whitelist validation.
"""

import os
import re
import sys
import hashlib
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app_core.config import (
    EXPORTS_DIR,
    UPLOADS_DIR,
    DOHNUT_PUBLIC_DIR,
    FFMPEG_TIMEOUT_SECONDS,
)

def create_tiktok_srt(script_text: str, duration: float, srt_filename: str) -> Path:
    """
    Creates an SRT subtitle file chunked by ~5-7 words or punctuation pauses.
    Calculates duration per chunk proportionally with min bounds.
    """
    words = script_text.strip().split()
    if not words:
        words = ["DOH-NUT", "The", "Artisanal", "Donut"]

    chunk_size = 6
    raw_chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    num_chunks = len(raw_chunks)
    time_per_chunk = max(0.8, duration / max(1, num_chunks))

    srt_path = EXPORTS_DIR / srt_filename
    with open(srt_path, "w", encoding="utf-8") as f:
        for idx, chunk in enumerate(raw_chunks, start=1):
            t_start = (idx - 1) * time_per_chunk
            t_end = min(duration, idx * time_per_chunk)
            if idx == num_chunks:
                t_end = max(duration, t_start + 0.5)

            h_s = int(t_start // 3600)
            m_s = int((t_start % 3600) // 60)
            s_s = int(t_start % 60)
            ms_s = int((t_start - int(t_start)) * 1000)

            h_e = int(t_end // 3600)
            m_e = int((t_end % 3600) // 60)
            s_e = int(t_end % 60)
            ms_e = int((t_end - int(t_end)) * 1000)

            f.write(f"{idx}\n")
            f.write(f"{h_s:02d}:{m_s:02d}:{s_s:02d},{ms_s:03d} --> {h_e:02d}:{m_e:02d}:{s_e:02d},{ms_e:03d}\n")
            f.write(f"{chunk}\n\n")

    return srt_path

def resolve_safe_video_path(bg_video_name: str) -> Path:
    """
    Resolves background video path safely against whitelisted directories,
    preventing path traversal.
    """
    safe_name = Path(bg_video_name).name
    # Check DOH-NUT public videos
    candidate_1 = DOHNUT_PUBLIC_DIR / "videos" / safe_name
    if candidate_1.exists() and candidate_1.is_file():
        return candidate_1

    # Check local uploads
    candidate_2 = UPLOADS_DIR / safe_name
    if candidate_2.exists() and candidate_2.is_file():
        return candidate_2

    # Fallback to any mp4 in DOH-NUT videos if candidate not found
    dohnut_videos = list((DOHNUT_PUBLIC_DIR / "videos").glob("*.mp4")) if (DOHNUT_PUBLIC_DIR / "videos").exists() else []
    if dohnut_videos:
        return dohnut_videos[0]

    # Fallback to any upload mp4
    upload_videos = list(UPLOADS_DIR.glob("*.mp4"))
    if upload_videos:
        return upload_videos[0]

    raise FileNotFoundError(f"No background video found matching '{safe_name}' in whitelisted locations.")

import shutil

ASPECT_CONFIGS = {
    "9:16": {"width": 720, "height": 1280, "fontsize": 22, "margin_v": 140},
    "1:1": {"width": 1080, "height": 1080, "fontsize": 26, "margin_v": 110},
    "16:9": {"width": 1280, "height": 720, "fontsize": 20, "margin_v": 70},
}

def render_vertical_video(
    audio_path_str: str,
    bg_video_name: str = "dohnut-hands-making-donut.mp4",
    script_text: str = "",
    target_width: Optional[int] = None,
    target_height: Optional[int] = None,
    aspect_ratio: str = "9:16",
) -> Dict[str, Any]:
    """
    Composites video with burned-in kinetic subtitles across 9:16, 1:1, and 16:9 aspect ratios.
    Uses atomic writes (.tmp.mp4 -> .mp4) and content hashing.
    Gracefully handles serverless cloud environments without local FFmpeg binaries.
    """
    audio_path = Path(audio_path_str)
    if not audio_path.is_absolute():
        audio_path = Path.cwd() / audio_path

    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    # Resolve aspect ratio configurations
    cfg = ASPECT_CONFIGS.get(aspect_ratio, ASPECT_CONFIGS["9:16"])
    if target_width is None:
        target_width = cfg["width"]
    if target_height is None:
        target_height = cfg["height"]
    fontsize = cfg["fontsize"]
    margin_v = cfg["margin_v"]

    # Safe background video resolution
    video_path = resolve_safe_video_path(bg_video_name)

    # Probe audio duration via ffprobe or estimate
    duration = 15.0
    if shutil.which("ffprobe"):
        cmd_probe = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(audio_path)
        ]
        try:
            probe_res = subprocess.run(cmd_probe, capture_output=True, text=True, timeout=10)
            duration = float(probe_res.stdout.strip())
        except Exception:
            pass

    # Cache key including audio content, video content, aspect ratio and script
    video_stat = video_path.stat()
    audio_stat = audio_path.stat()
    cache_signature = f"{video_path.name}_{video_stat.st_size}_{video_stat.st_mtime}_{audio_path.name}_{audio_stat.st_size}_{aspect_ratio}_{target_width}x{target_height}_{script_text.strip()}"
    content_hash = hashlib.md5(cache_signature.encode("utf-8")).hexdigest()[:10]

    video_stem = re.sub(r'[^a-zA-Z0-9_-]', '_', video_path.stem)
    audio_stem = re.sub(r'[^a-zA-Z0-9_-]', '_', audio_path.stem)
    aspect_tag = aspect_ratio.replace(":", "x")
    out_filename = f"render_{audio_stem}_{video_stem}_{aspect_tag}_{content_hash}.mp4"
    out_path = EXPORTS_DIR / out_filename

    # If already rendered and valid, return cached file immediately
    if out_path.exists() and out_path.stat().st_size > 10000:
        return {
            "status": "cached",
            "video_url": f"/exports/{out_filename}",
            "filename": out_filename,
            "duration": round(duration, 2),
            "width": target_width,
            "height": target_height,
            "aspect_ratio": aspect_ratio,
        }

    # Generate SRT
    srt_filename = f"sub_{content_hash}.srt"
    create_tiktok_srt(script_text, duration, srt_filename)

    # Serverless check: If FFmpeg binary is not present in container/OS, return serverless manifest
    if not shutil.which("ffmpeg"):
        return {
            "status": "serverless_ready",
            "video_url": f"/videos/{video_path.name}" if "videos" in str(video_path) else f"/static/uploads/{video_path.name}",
            "audio_url": f"/exports/{audio_path.name}",
            "srt_url": f"/exports/{srt_filename}",
            "duration": round(duration, 2),
            "width": target_width,
            "height": target_height,
            "aspect_ratio": aspect_ratio,
            "engine": "In-Browser Synchronized Playback (Serverless Mode)",
            "note": "Persekitaran awan Vercel: Audio Azure & sari kata kinetik sedia dimainkan serentak dalam pelayar."
        }

    rel_srt = f"static/exports/{srt_filename}"
    temp_out_path = EXPORTS_DIR / f"temp_{out_filename}"

    # TikTok Yellow Caption styling adapted to aspect ratio
    filter_complex = (
        f"scale={target_width}:{target_height}:force_original_aspect_ratio=increase,"
        f"crop={target_width}:{target_height},"
        f"subtitles={rel_srt}:force_style='Fontname=Arial\\,Fontsize={fontsize}\\,Bold=1\\,PrimaryColour=&H0000FFFF\\,OutlineColour=&H00000000\\,BorderStyle=1\\,Outline=2.5\\,Shadow=1\\,Alignment=2\\,MarginV={margin_v}'"
    )

    cmd_ffmpeg = [
        "ffmpeg", "-y",
        "-threads", "0",
        "-stream_loop", "-1",
        "-i", str(video_path),
        "-i", str(audio_path),
        "-t", str(duration),
        "-vf", filter_complex,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-tune", "zerolatency",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "128k",
        "-shortest",
        str(temp_out_path)
    ]

    res = subprocess.run(cmd_ffmpeg, capture_output=True, text=True, timeout=FFMPEG_TIMEOUT_SECONDS)
    if res.returncode != 0:
        if temp_out_path.exists():
            temp_out_path.unlink()
        raise RuntimeError(f"FFmpeg execution failed (code {res.returncode}): {res.stderr[-500:]}")

    # Atomic rename to final output
    temp_out_path.rename(out_path)

    return {
        "status": "success",
        "video_url": f"/exports/{out_filename}",
        "filename": out_filename,
        "duration": round(duration, 2),
        "width": target_width,
        "height": target_height,
        "aspect_ratio": aspect_ratio,
    }
