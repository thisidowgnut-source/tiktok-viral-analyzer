"""
Google GenAI / AI Studio Server-Side Adapter for ViralStudio.
Uses official google-genai SDK (v1.x) with strict request/response validation,
rate-limit resilience, telemetry capture, and deterministic offline mock fallback.
Adheres to Prompt G7 specifications.
"""

import os
import time
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

try:
    from google import genai
    from google.genai import types
    from google.genai.errors import APIError
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


class ScriptScenePlan(BaseModel):
    scene_index: int = Field(..., description="0-indexed scene order")
    narration: str = Field(..., description="Spoken voiceover text in Bahasa Melayu")
    visual_cue: str = Field(..., description="Visual camera direction or b-roll action")
    on_screen_text: str = Field(..., description="Short kinetic subtitle or overlay headline")
    duration_est: float = Field(default=3.5, description="Estimated duration in seconds")


class StructuredBriefResponse(BaseModel):
    campaign_title: str
    target_audience: str
    core_hook: str
    scenes: List[ScriptScenePlan]
    estimated_total_duration: float
    model_id: str
    tokens_used: Dict[str, int]
    latency_ms: float
    is_mock: bool = False
    blocker_note: Optional[str] = None


class GoogleAIStudioAdapter:
    """
    Production-ready server-side adapter for Google Gemini models.
    Separates credentials into environment variables, protects against key leaks,
    and provides a deterministic offline path if credentials are missing or rate-limited.
    """

    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-2.5-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.model_name = model_name
        self.client = None

        if GENAI_AVAILABLE and self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"[!] Warning: Failed to initialize Google GenAI client: {e}")
                self.client = None

    def is_configured(self) -> bool:
        """Returns True if Google GenAI client is actively configured with valid credentials."""
        return self.client is not None

    def generate_scene_plan(
        self,
        product_name: str,
        angle: str,
        target_duration: int = 15,
        brand_tone: str = "Energetic, authentic Malaysian youth tone"
    ) -> StructuredBriefResponse:
        """
        Generates a structured video scene breakdown using Google Gemini,
        or falls back gracefully to a curated ground-truth template if unconfigured.
        """
        t0 = time.perf_counter()

        # If not configured, use the deterministic offline mock path
        if not self.client:
            return self._generate_offline_mock(product_name, angle, target_duration, t0)

        prompt = f"""
Anda adalah pengarah video pendek profesional TikTok/Reels untuk pasaran Malaysia.
Hasilkan skrip video pendek berdurasi anggaran {target_duration} saat untuk produk '{product_name}' dengan sudut kempen '{angle}'.
Gaya bahasa: {brand_tone} (Bahasa Melayu moden).

Berikan output dalam format JSON sah dengan struktur:
{{
  "campaign_title": "Tajuk Kempen",
  "target_audience": "Sasaran audiens utama",
  "core_hook": "Ayat hook 3 saat pertama",
  "scenes": [
    {{
      "scene_index": 0,
      "narration": "Skrip suara yang dibaca",
      "visual_cue": "Arahan visual kamera/aksi produk",
      "on_screen_text": "Teks atas skrin (maksimum 4-6 perkataan)",
      "duration_est": 3.5
    }}
  ]
}}
"""
        max_retries = 2
        backoff_sec = 1.0

        for attempt in range(max_retries + 1):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.7,
                        response_mime_type="application/json"
                    )
                )

                latency_ms = round((time.perf_counter() - t0) * 1000, 2)
                raw_text = response.text or "{}"
                data = json.loads(raw_text)

                scenes = [
                    ScriptScenePlan(
                        scene_index=idx,
                        narration=s.get("narration", ""),
                        visual_cue=s.get("visual_cue", ""),
                        on_screen_text=s.get("on_screen_text", ""),
                        duration_est=float(s.get("duration_est", 3.5))
                    )
                    for idx, s in enumerate(data.get("scenes", []))
                ]

                # Extract token usage if available in metadata
                tokens = {"prompt": 0, "candidates": 0, "total": 0}
                if hasattr(response, "usage_metadata") and response.usage_metadata:
                    um = response.usage_metadata
                    tokens["prompt"] = getattr(um, "prompt_token_count", 0) or 0
                    tokens["candidates"] = getattr(um, "candidates_token_count", 0) or 0
                    tokens["total"] = getattr(um, "total_token_count", 0) or 0

                return StructuredBriefResponse(
                    campaign_title=data.get("campaign_title", f"{product_name} - {angle}"),
                    target_audience=data.get("target_audience", "Pencinta manisan & pengguna media sosial"),
                    core_hook=data.get("core_hook", scenes[0].narration if scenes else ""),
                    scenes=scenes,
                    estimated_total_duration=sum(s.duration_est for s in scenes),
                    model_id=self.model_name,
                    tokens_used=tokens,
                    latency_ms=latency_ms,
                    is_mock=False
                )

            except Exception as e:
                err_msg = str(e)
                if ("429" in err_msg or "ResourceExhausted" in err_msg) and attempt < max_retries:
                    time.sleep(backoff_sec)
                    backoff_sec *= 2
                    continue

                # Return offline fallback with explicit blocker explanation
                return self._generate_offline_mock(
                    product_name, angle, target_duration, t0,
                    blocker=f"Google API Error: {type(e).__name__} ({err_msg})"
                )

        return self._generate_offline_mock(product_name, angle, target_duration, t0, blocker="Max retries reached")

    def _generate_offline_mock(
        self,
        product_name: str,
        angle: str,
        target_duration: int,
        t0: float,
        blocker: Optional[str] = None
    ) -> StructuredBriefResponse:
        """
        Deterministic, offline ground-truth fallback matching DOH-NUT campaign standards.
        Never blocks the user workflow when cloud API keys are absent.
        """
        latency_ms = round((time.perf_counter() - t0) * 1000, 2)
        if not blocker:
            blocker = "TIADA_API_KEY: Menggunakan enjin templat tempatan (tiada caj API)"

        mock_scenes = [
            ScriptScenePlan(
                scene_index=0,
                narration=f"Sound on! Dengar bunyi krup-krap kerak doh panas {product_name} ni sebelum inti dia leleh!",
                visual_cue="Extreme close-up picit donat, krim melimpah keluar secara perlahan.",
                on_screen_text="DOH CRUNCH SOUND ON 🔊",
                duration_est=3.5
            ),
            ScriptScenePlan(
                scene_index=1,
                narration="Tengok bila kita picit lembut je donat brioche ni, inti pekat melimpah ruah panas-panas.",
                visual_cue="Macro shot lelehan krim jatuh ke pinggan seramik.",
                on_screen_text="LELEHAN MELELEH PANAS 🤤",
                duration_est=4.0
            ),
            ScriptScenePlan(
                scene_index=2,
                narration="Doh brioche sourdough fermentasi 48 jam yang sangat gebu, rangup di luar dan lembut di dalam.",
                visual_cue="Belahan rentas tekstur sarang doh berongga lembut.",
                on_screen_text="FERMENTASI 48 JAM 🍞",
                duration_est=4.0
            ),
            ScriptScenePlan(
                scene_index=3,
                narration="Free delivery kalau order atas RM25! Tekan beg kuning kat bawah sekarang sebelum sold out!",
                visual_cue="Kotak oren dohnut bertutup rapi bersedia diikat pita jenama.",
                on_screen_text="ORDER KAT BEG KUNING 🛍️",
                duration_est=3.5
            )
        ]

        return StructuredBriefResponse(
            campaign_title=f"{product_name} - {angle} (Local Baseline)",
            target_audience="Penggemar donat artisan & pencari snek petang pejabat",
            core_hook=mock_scenes[0].narration,
            scenes=mock_scenes,
            estimated_total_duration=sum(s.duration_est for s in mock_scenes),
            model_id="offline-dohnut-template-engine",
            tokens_used={"prompt": 0, "candidates": 0, "total": 0},
            latency_ms=latency_ms,
            is_mock=True,
            blocker_note=blocker
        )
