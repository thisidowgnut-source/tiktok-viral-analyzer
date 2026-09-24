"""
ViralStudio KA-363 (Enterprise Edition v3.0)
Flagship PWA + In-Browser Teleprompter + Doh-Nut Proven Campaign Arsenal
Features:
1. PWA Installability (manifest.json, Service Worker sw.js, app icons)
2. Live In-Browser Teleprompter Studio (Auto-scroll, Speed, Font Size, Mirror Mode)
3. Doh-Nut 4-Angle Master Campaign Arsenal (Hypebeast Unboxing, Sambal Burger, 3PM Slump, ASMR Lava)
4. A2A (Agent-to-Agent) Multi-Agent Collaborative Arena (Zara + Tariq + Sam)
5. 363-Video Intelligence Hub & Scatter Plot (@khairulaming benchmark)
6. Jev Realtime Virality Scorer & Khairul Aming Script Generator
"""

import sys
import os
import json
import asyncio
import hashlib
import subprocess
from pathlib import Path
from typing import Optional, List
import edge_tts
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import modular engines & routers
from virality_scorer import evaluate_script
from viral_script_generator import generate_viral_script
from a2a_engine import run_a2a_collaboration, handle_copilot_chat, DOHNUT_KNOWLEDGE
from db.migrations import run_migrations
from api.projects_router import router as projects_router
from api.assets_router import router as assets_router
from api.jobs_router import router as jobs_router
from api.integrations_router import router as integrations_router

BASE_DIR = Path(os.getenv("VIRALSTUDIO_BASE_DIR", Path(__file__).resolve().parent))
STATIC_DIR = BASE_DIR / "static"
EXPORTS_DIR = STATIC_DIR / "exports"
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
UPLOADS_DIR = STATIC_DIR / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
DATA_363_PATH = BASE_DIR / "khairulaming_all_363_analysis.json"

app = FastAPI(
    title="ViralStudio KA-363",
    description="PWA Viral Retention Engine, Doh-Nut Campaigns & Teleprompter Studio",
    version="3.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount modular REST routers
app.include_router(projects_router)
app.include_router(assets_router)
app.include_router(jobs_router)
app.include_router(integrations_router)

@app.on_event("startup")
def startup_event():
    run_migrations()

# Mount static folder for PWA, uploads and exports
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
if EXPORTS_DIR.exists():
    app.mount("/exports", StaticFiles(directory=str(EXPORTS_DIR)), name="exports")

DOHNUT_PUBLIC_DIR = Path(os.getenv("DOHNUT_PUBLIC_DIR", BASE_DIR.parent / "Doh-Nut" / "public"))
if (DOHNUT_PUBLIC_DIR / "brand").exists():
    app.mount("/brand", StaticFiles(directory=str(DOHNUT_PUBLIC_DIR / "brand")), name="brand")
if (DOHNUT_PUBLIC_DIR / "videos").exists():
    app.mount("/videos", StaticFiles(directory=str(DOHNUT_PUBLIC_DIR / "videos")), name="videos")

# Load 363 dataset into memory
ALL_VIDEOS = []
MACRO_STATS = {
    "total_videos": 363,
    "total_views": 213389111,
    "total_likes": 18689897,
    "total_shares": 1354838,
    "categories": {"RESEPI_RAMADAN": 343, "BEHIND_THE_SCENES_BISNES": 16, "RESEPI_VIRAL_HARIAN": 4}
}

if DATA_363_PATH.exists():
    try:
        with open(DATA_363_PATH, "r", encoding="utf-8") as f:
            ALL_VIDEOS = json.load(f)
    except Exception as e:
        print(f"[!] Warning: Could not load 363 videos JSON: {e}")

# Curated Doh-Nut Ground-Truth Playbook Campaigns (Aligned with 31-Flavor Catalog)
DOHNUT_CAMPAIGNS = [
    {
        "id": "dohnut_nutella_lava",
        "title": "🍫 Nutella Hazelnut Lava — The Molten Eruption",
        "angle": "ASMR Tactile Macro Sensory",
        "flavor": "Nutella Hazelnut Lava (RM 5.20)",
        "hook_style": "CRAVING_SENSORY",
        "score": 9.7,
        "tier": "🏆 SOTA VIRAL TIER",
        "retention_rate": "89%",
        "hook_verbatim": "Sound on! Dengar bunyi krup-krap kerak doh panas ni sebelum lava Nutella dia memancut...",
        "script": "Sound on! Dengar bunyi krup-krap kerak doh panas ni sebelum lava Nutella dia memancut! Tengok bila kita picit lembut je donat brioche DOH-NUT ni, inti coklat hazelnut pekat meleleh melimpah ruah panas-panas. Taburan kacang hazelnut bakar dia bagi crunch gila setiap kunyahan. Ini bukan donut biasa, ini 'GOOD VIBE. GOOD DOH.' yang dibakar fresh setiap pagi! Order atas RM25 dapat free delivery terus sampai pintu dalam 25 minit. DOH NUT WAIT, tekan beg kuning kat bawah sekarang!",
        "camera_direction": "ECU 4K 60fps Macro — Tekanan ibu jari menembusi permukaan doh, limpahan lava Nutella pekat membuak keluar.",
        "sfx": "SFX: Crunchy crust snap pada 0.3s + creamy squelch limpahan coklat.",
        "image": "/brand/donuts/donut_stuffed1.png"
    },
    {
        "id": "dohnut_hypebeast_drop",
        "title": "📦 The Hypebeast Streetwear Box Drop Unboxing",
        "angle": "Streetwear Sneaker Drop Culture",
        "flavor": "Musang King Durian Bomb (RM 6.50) & Curated Dozen",
        "hook_style": "CRAVING_SENSORY",
        "score": 9.5,
        "tier": "🏆 SOTA VIRAL TIER",
        "retention_rate": "85%",
        "hook_verbatim": "Korang bayangkan beli donut tapi rasa macam tengah unbox sneaker limited edition!",
        "script": "Korang bayangkan beli donut tapi rasa macam tengah unbox sneaker limited edition! Ini DOH-NUT! Bukan donut biasa yang liat atau manis leting. Tengok doh dia, gebu melantun macam kapas, dan glaze dia dibuat fresh setiap pagi. Paling gila perisa Musang King Durian Bomb ni... guna 100% puri durian Raub asli, filling kastard durian dia meleleh tak kedekut langsung! Free delivery kalau order atas RM25! Tekan beg kuning atau klik link kat bio sekarang sebelum drop hari ni sold out!",
        "camera_direction": "Medium Shot — Hentakan kotak kuning kemas atas meja kafe, buka penutup dramatik.",
        "sfx": "SFX: Bass thud kotak + zipper slide.",
        "image": "/brand/donuts/musang-king-durian.png"
    },
    {
        "id": "dohnut_sambal_burger",
        "title": "🌶️ Donut Sambal Bilis?! Real or Cap?",
        "angle": "Malaysian Street Food Shock & Awe",
        "flavor": "Kuih Burger Malaysia (RM 5.50)",
        "hook_style": "STORY_CURIOSITY",
        "score": 9.4,
        "tier": "🏆 SOTA VIRAL TIER",
        "retention_rate": "83%",
        "hook_verbatim": "Siapa yang berani sangat belah donut gebu lepastu sumbat sambal bilis pedas berapi macam ni?!",
        "script": "Siapa yang berani sangat belah donut gebu lepastu sumbat sambal bilis pedas berapi macam ni?! Mula-mula aku ingat sekadar gimmick viral, tapi bila gigit... gabungan donut lembut manis dengan sambal bilis pedas-manis berkilat dan timun rangup ni serius padu teruk! Tekstur bilis garing krup krap bersatu dengan kegebuan doh artisan. Ada 31 perisa lokal lain yang korang takkan jumpa kat tempat lain macam Teh Tarik Kaw dan Pandan Melaka. Kena try sendiri kat link bio!",
        "camera_direction": "Eye-level 45° — Pegang donut burger depan kamera, tunjuk hirisan timun dan sambal bilis berkilat.",
        "sfx": "SFX: Gigitan rangup ikan bilis crunch + muzik beat rancak.",
        "image": "/brand/donuts/kuih-burger-malaysia.png"
    },
    {
        "id": "dohnut_sira_keria",
        "title": "🍯 Sira Kuih Keria — Gula Melaka Crackle ASMR",
        "angle": "Heritage Tradition Meets Modern Streetwear",
        "flavor": "Sira Kuih Keria (RM 4.90) & Sira Sambal (RM 5.20)",
        "hook_style": "CRAVING_SENSORY",
        "score": 9.3,
        "tier": "🏆 SOTA VIRAL TIER",
        "retention_rate": "80%",
        "hook_verbatim": "Dengar bunyi kristal gula melaka ni bila kita gigit... krup!",
        "script": "Dengar bunyi kristal gula melaka ni bila kita gigit... krup! Ini Sira Kuih Keria DOH-NUT! Selaput gula Melaka amber berkilau yang nipis dan rangup di luar, tapi bila sampai kat doh... ya ampun gebu lembut gila! Disalut sira gula Melaka asli yang pekat berkaramel. Ada juga versi pedas berapi Sira Sambal bersalut bijan bakar. Warisan kuih Melayu versi moden streetwear. DOH GILER sedap! Korang boleh tap beg kuning kat bawah!",
        "camera_direction": "Macro Shot — Cahaya memantul pada rekahan kristal gula Melaka warna amber keemasan.",
        "sfx": "SFX: Delicate sugar glaze cracking sound.",
        "image": "/brand/donuts/sira-kuih-keria.png"
    },
    {
        "id": "dohnut_3pm_slump",
        "title": "☕ Penyelamat Slump 3 Petang Pejabat",
        "angle": "Office Group Order & B2B Craving",
        "flavor": "Pandan Gula Melaka (RM 4.90) & Teh Tarik Kaw (RM 4.80)",
        "hook_style": "EMPATHY_RELATABLE",
        "score": 9.2,
        "tier": "⚡ HIGH-PERFORMER TIER",
        "retention_rate": "79%",
        "hook_verbatim": "Setiap kali pukul 3 petang kat office, mata confirm layu dan craving benda manis...",
        "script": "Setiap kali pukul 3 petang kat office, mata confirm layu dan craving benda manis... Terus kitorang order Doh-Nut 2 dozen! Panas-panas rider hantar, bau wangi pandan dan teh tarik semerbak satu office, terus segar balik otak nak sambung kerja. Order atas RM25 dapat free delivery terus sampai lobi. Korang yang tengah pening nak makan apa petang ni, order sekarang kat link bio sebelum jam 4 petang!",
        "camera_direction": "Overhead Shot — Jam dinding 3:15 PM, rakan sekerja bawa 2 kotak besar, serbuan meja.",
        "sfx": "Muzik ceria bertenaga.",
        "image": "/brand/donuts/pandan-gula-melaka.png"
    }
]


# Pydantic Schemas
class ScoreRequest(BaseModel):
    script: str

class GenerateRequest(BaseModel):
    product_name: str
    niche: Optional[str] = "Makanan / F&B"
    hook_style: Optional[str] = "CRAVING_SENSORY"
    target_audience: Optional[str] = "Keluarga & Gen-Z TikTok Malaysia"
    usp_points: Optional[List[str]] = None
    include_catchphrase: Optional[bool] = True

class A2ARequest(BaseModel):
    prompt: str

class ChatRequest(BaseModel):
    message: str

class TTSRequest(BaseModel):
    text: str
    voice: Optional[str] = "ms-MY-YasminNeural"
    rate: Optional[str] = "+0%"

class RenderVideoRequest(BaseModel):
    script_text: str
    product_name: Optional[str] = "Doh-Nut"
    voice: Optional[str] = "ms-MY-YasminNeural"
    rate: Optional[str] = "+0%"
    bg_video: Optional[str] = "dohnut-hands-making-donut.mp4"


# Cloud-streamed Neural Voiceover (Microsoft Azure Speech via edge-tts, requires internet connection)
async def synthesize_speech(text: str, voice: str = "ms-MY-YasminNeural", rate: str = "+0%") -> tuple:
    """Synthesizes speech using Microsoft Azure Speech network service via edge-tts."""
    text_clean = text.strip()
    text_hash = hashlib.md5(f"{text_clean}_{voice}_{rate}".encode("utf-8")).hexdigest()[:12]
    audio_filename = f"tts_{text_hash}.mp3"
    audio_path = EXPORTS_DIR / audio_filename
    if not audio_path.exists():
        comm = edge_tts.Communicate(text_clean, voice, rate=rate)
        await comm.save(str(audio_path))
    
    cmd_probe = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)]
    try:
        dur = float(subprocess.check_output(cmd_probe).decode().strip())
    except Exception:
        dur = 10.0
    return audio_filename, dur


def create_tiktok_srt(script_text: str, duration: float, srt_filename: str) -> Path:
    """Generates kinetic 5-7 word subtitle chunks with TikTok styling and timing."""
    words = script_text.strip().split()
    if not words:
        words = ["DOH-NUT", "Brioche", "Fresh", "Viral"]

    chunk_size = 6
    chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    num_chunks = len(chunks)
    time_per_chunk = max(0.5, duration / max(1, num_chunks))

    def fmt_srt_time(sec: float) -> str:
        h = int(sec // 3600)
        m = int((sec % 3600) // 60)
        s = int(sec % 60)
        ms = int(round((sec - int(sec)) * 1000))
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    lines = []
    for idx, chunk in enumerate(chunks, start=1):
        t_start = (idx - 1) * time_per_chunk
        t_end = min(duration, idx * time_per_chunk)
        lines.append(str(idx))
        lines.append(f"{fmt_srt_time(t_start)} --> {fmt_srt_time(t_end)}")
        lines.append(chunk)
        lines.append("")

    srt_path = EXPORTS_DIR / srt_filename
    srt_path.write_text("\n".join(lines), encoding="utf-8")
    return srt_path


def render_vertical_video(audio_filename: str, duration: float, bg_video_name: str = "dohnut-hands-making-donut.mp4", script_text: str = "") -> str:
    """Renders vertical 9:16 TikTok video with burned-in kinetic subtitles using multithreaded FFmpeg."""
    audio_path = EXPORTS_DIR / audio_filename
    video_in = DOHNUT_PUBLIC_DIR / "videos" / bg_video_name
    if not video_in.exists():
        vids = list((DOHNUT_PUBLIC_DIR / "videos").glob("*.mp4"))
        video_in = vids[0] if vids else video_in

    # Uniquely hash all input dependencies to completely prevent cache collision (Issue 1)
    video_stem = Path(bg_video_name).stem.replace("-", "_")
    audio_stem = audio_filename.replace(".mp3", "")
    sub_hash = hashlib.md5(script_text.strip().encode("utf-8")).hexdigest()[:8]
    out_filename = f"render_{audio_stem}_{video_stem}_{sub_hash}.mp4"
    out_path = EXPORTS_DIR / out_filename

    if out_path.exists() and out_path.stat().st_size > 1000:
        return out_filename

    # Generate kinetic subtitles file (Issue 2)
    srt_filename = f"sub_{sub_hash}.srt"
    create_tiktok_srt(script_text, duration, srt_filename)

    # Relative path for FFmpeg on Windows to prevent colon drive letter parsing errors
    rel_srt_path = f"static/exports/{srt_filename}"

    # TikTok yellow text (&H0000FFFF), bold, black outline (&H00000000), bottom-third alignment (MarginV=140)
    sub_filter = (
        f"subtitles={rel_srt_path}:force_style=Fontname=Arial\\,Fontsize=22\\,Bold=1\\,"
        f"PrimaryColour=&H0000FFFF\\,OutlineColour=&H00000000\\,BorderStyle=1\\,Outline=2.5\\,"
        f"Shadow=1\\,Alignment=2\\,MarginV=140"
    )

    filter_complex = f"[0:v]crop=ih*9/16:ih:(iw-ih*9/16)/2:0,scale=720:1280,{sub_filter},format=yuv420p[v]"

    cmd_ffmpeg = [
        "ffmpeg", "-y",
        "-threads", "0",
        "-stream_loop", "-1",
        "-i", str(video_in),
        "-i", str(audio_path),
        "-t", str(duration),
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-map", "1:a",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-tune", "zerolatency",
        "-crf", "25",
        "-c:a", "aac",
        "-b:a", "128k",
        "-shortest",
        str(out_path)
    ]
    res = subprocess.run(cmd_ffmpeg, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"FFmpeg error: {res.stderr[:300]}")
    return out_filename


@app.get("/api/stats")
async def get_stats():
    return JSONResponse(MACRO_STATS)


@app.get("/sw.js")
async def serve_root_service_worker():
    """Serves service worker from root with Service-Worker-Allowed header to enable root scope."""
    sw_file = STATIC_DIR / "sw.js"
    if sw_file.exists():
        return FileResponse(
            str(sw_file),
            media_type="application/javascript",
            headers={"Service-Worker-Allowed": "/"}
        )
    raise HTTPException(status_code=404, detail="Service worker not found")


@app.get("/api/videos")
async def get_videos(limit: int = 363, hook: Optional[str] = None, q: Optional[str] = None):
    results = ALL_VIDEOS
    if hook and hook != "ALL":
        results = [v for v in results if (v.get("hook_type") or v.get("hook_analysis", {}).get("hook_type")) == hook]
    if q:
        query = q.lower()
        results = [
            v for v in results
            if query in v.get("title", "").lower()
            or query in (v.get("hook_verbatim") or v.get("hook_analysis", {}).get("hook_verbatim", "")).lower()
        ]
    return JSONResponse(results[:limit])


@app.post("/api/score")
async def score_script(req: ScoreRequest):
    if not req.script.strip():
        raise HTTPException(status_code=400, detail="Skrip tidak boleh kosong.")
    res = evaluate_script(req.script)
    return JSONResponse(res)


@app.post("/api/generate")
async def generate_script_endpoint(req: GenerateRequest):
    if not req.product_name.strip():
        raise HTTPException(status_code=400, detail="Nama produk wajib diisi.")
    res = generate_viral_script(
        product_name=req.product_name,
        niche=req.niche or "Makanan / F&B",
        hook_style=req.hook_style or "CRAVING_SENSORY",
        target_audience=req.target_audience or "Keluarga & Gen-Z TikTok Malaysia",
        usp_points=req.usp_points,
        include_catchphrase=req.include_catchphrase
    )
    return JSONResponse(res)


@app.get("/api/dohnut/campaigns")
async def get_dohnut_campaigns():
    return JSONResponse({
        "knowledge": DOHNUT_KNOWLEDGE,
        "campaigns": DOHNUT_CAMPAIGNS
    })


@app.post("/api/a2a/collaborate")
async def a2a_collaborate(req: A2ARequest):
    if not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt kolaborasi wajib diisi.")
    res = run_a2a_collaboration(req.prompt)
    return JSONResponse(res)


@app.post("/api/a2a/chat")
async def a2a_chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Mesej chat wajib diisi.")
    res = handle_copilot_chat(req.message)
    return JSONResponse(res)


@app.post("/api/tts")
async def generate_tts(req: TTSRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Teks untuk suara tidak boleh kosong.")
    try:
        audio_fn, dur = await synthesize_speech(req.text, req.voice or "ms-MY-YasminNeural", req.rate or "+0%")
        return JSONResponse({
            "status": "success",
            "audio_url": f"/exports/{audio_fn}",
            "duration": round(dur, 2),
            "voice": req.voice
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ralat penjanaan suara: {e}")


@app.post("/api/render-video")
async def render_video_endpoint(req: RenderVideoRequest):
    if not req.script_text.strip():
        raise HTTPException(status_code=400, detail="Skrip video tidak boleh kosong.")
    try:
        audio_fn, dur = await synthesize_speech(req.script_text, req.voice or "ms-MY-YasminNeural", req.rate or "+0%")
        # Non-blocking async thread execution to keep main event loop responsive (Issue 4)
        video_fn = await asyncio.to_thread(
            render_vertical_video,
            audio_filename=audio_fn,
            duration=dur,
            bg_video_name=req.bg_video or "dohnut-hands-making-donut.mp4",
            script_text=req.script_text
        )
        return JSONResponse({
            "status": "success",
            "video_url": f"/exports/{video_fn}",
            "duration": round(dur, 2),
            "filename": video_fn,
            "product": req.product_name,
            "voice": req.voice
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ralat render video FFmpeg: {e}")


@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    """Serves the rich modern unified web app from templates/index.html."""
    template_path = BASE_DIR / "templates" / "index.html"
    if template_path.exists():
        with open(template_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>ViralStudio Index Not Found</h1>", status_code=404)


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8765))
    print(f"[*] Starting ViralStudio KA-363 PWA & Teleprompter Web Server on http://localhost:{port}")
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="info")
