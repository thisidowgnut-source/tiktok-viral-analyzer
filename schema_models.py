"""
TypeSafe Pydantic V2 Schema Models for TikTok Video Retention & Structure Analysis.
Compatible with OpenAI Structured Outputs (strict=True), Gemini response_schema, and TypeSafe AI.
"""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class TopicCategory(str, Enum):
    RESEPI_RAMADAN = "RESEPI_RAMADAN"
    RESEPI_VIRAL_HARIAN = "RESEPI_VIRAL_HARIAN"
    TRAVELOG_VLOG = "TRAVELOG_VLOG"
    BEHIND_THE_SCENES_BISNES = "BEHIND_THE_SCENES_BISNES"
    COMMUNITY_CSR = "COMMUNITY_CSR"


class HookType(str, Enum):
    CRAVING_SENSORY = "CRAVING_SENSORY"
    SIGNATURE_GREETING = "SIGNATURE_GREETING"
    STORY_CURIOSITY = "STORY_CURIOSITY"
    DIRECT_VALUE = "DIRECT_VALUE"
    EMPATHY_RELATABLE = "EMPATHY_RELATABLE"


class StructureTag(str, Enum):
    HOOK = "HOOK"
    SETUP = "SETUP"
    PAYOFF = "PAYOFF"
    PITCH = "PITCH"


class PacingSpeed(str, Enum):
    RAPID_FIRE = "RAPID_FIRE"
    MODERATE_RHYTHMIC = "MODERATE_RHYTHMIC"
    NARRATIVE_SLOW = "NARRATIVE_SLOW"


class HookAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    hook_type: HookType = Field(..., description="Klasifikasi jenis hook pembuka (3-5 saat pertama)")
    hook_verbatim: str = Field(..., description="Ayat pembuka penuh yang dituturkan")
    word_count: int = Field(..., description="Jumlah perkataan dalam ayat pembuka")
    has_signature_catchphrase: bool = Field(..., description="Mengandungi variasi Hey what's up guys atau frasa ikonik")


class StructureItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    order: int = Field(..., description="Nombor turutan ayat bermula dari 1")
    tag: StructureTag = Field(..., description="Label peranan ayat: HOOK, SETUP, PAYOFF, atau PITCH")
    text: str = Field(..., description="Teks ayat penuh")


class TikTokVideoAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    video_id: str = Field(..., description="Pengenal unik video (contoh: KA_001)")
    topic_category: TopicCategory = Field(..., description="Kategori topik kandungan video")
    hook_analysis: HookAnalysis = Field(..., description="Analisis terperinci ayat pembuka")
    structure_breakdown: List[StructureItem] = Field(..., description="Senarai pemecahan ayat demi ayat berlabel")
    pacing_speed: PacingSpeed = Field(..., description="Rentak kelajuan suntingan dan lontaran suara")
    retention_mechanisms: List[str] = Field(..., description="Senarai faktor psikologi yang menahan penonton tidak swipe away")
    closing_call_to_action: Optional[str] = Field(None, description="Teks seruan bertindak penutup atau null jika tiada")
    viral_factor_summary: str = Field(..., description="Ringkasan 1-2 ayat mengapa struktur video ini berkesan")


if __name__ == "__main__":
    import json
    schema = TikTokVideoAnalysis.model_json_schema()
    print(json.dumps(schema, indent=2))
