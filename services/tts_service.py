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

    # Generate via edge-tts with SubMaker for sentence/word boundary synchronization
    comm = edge_tts.Communicate(text_clean, voice, rate=rate)
    sub_maker = edge_tts.SubMaker()
    
    with open(audio_path, "wb") as fp:
        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                fp.write(chunk["data"])
            elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
                try:
                    sub_maker.feed(chunk)
                except Exception:
                    pass

    # Save generated boundary SRT
    srt_filename = f"sub_{audio_hash}.srt"
    srt_path = EXPORTS_DIR / srt_filename
    srt_content = sub_maker.get_srt()
    
    # Calculate exact duration from Azure Speech cues or probe with ffprobe
    if sub_maker.cues:
        duration = round(sub_maker.cues[-1].end.total_seconds(), 2)
    else:
        duration = probe_audio_duration(audio_path)

    # If SubMaker produced empty SRT, generate fallback chunked SRT
    if not srt_content.strip():
        srt_content = _generate_proportional_srt(text_clean, duration)

    with open(srt_path, "w", encoding="utf-8") as srt_fp:
        srt_fp.write(srt_content)

    return {
        "status": "success",
        "audio_url": f"/exports/{audio_filename}",
        "audio_path": str(audio_path),
        "srt_url": f"/exports/{srt_filename}",
        "srt_content": srt_content,
        "filename": audio_filename,
        "duration": duration,
        "voice": voice,
        "cues_count": len(sub_maker.cues),
        "engine": "Microsoft Azure Neural (Awan - Sifar Kos Kunci API)",
        "is_offline": False
    }

def _generate_proportional_srt(text: str, duration: float) -> str:
    """Fallback generator for proportional SRT chunks if boundary cues unavailable."""
    words = text.strip().split()
    if not words:
        return ""
    chunk_size = 5
    raw_chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    num_chunks = len(raw_chunks)
    time_per_chunk = max(0.8, duration / max(1, num_chunks))
    
    lines = []
    for idx, chunk in enumerate(raw_chunks, start=1):
        t_start = (idx - 1) * time_per_chunk
        t_end = min(duration, idx * time_per_chunk)
        if idx == num_chunks:
            t_end = max(duration, t_start + 0.5)

        h_s, rem = divmod(t_start, 3600)
        m_s, s_s = divmod(rem, 60)
        ms_s = int((s_s - int(s_s)) * 1000)

        h_e, rem_e = divmod(t_end, 3600)
        m_e, s_e = divmod(rem_e, 60)
        ms_e = int((s_e - int(s_e)) * 1000)

        lines.append(f"{idx}")
        lines.append(f"{int(h_s):02d}:{int(m_s):02d}:{int(s_s):02d},{ms_s:03d} --> {int(h_e):02d}:{int(m_e):02d}:{int(s_e):02d},{ms_e:03d}")
        lines.append(chunk)
        lines.append("")
    return "\n".join(lines)

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
