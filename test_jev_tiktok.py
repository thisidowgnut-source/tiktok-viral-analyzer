"""
TypeSafe AI Jev System One Integration for TikTok Video Script Dissection.
Leverages Jev primitives (Choice, Score, Noul) with sub-10ms calibrated probabilities.
"""

import sys
import os
import json
import time

# Add typesafe-system-one to sys.path
sys.path.insert(0, r"C:\Users\User\projects\typesafe-system-one")

from core import TypeSafeClient, Choice, Score, Noul

def analyze_with_jev(transcript: str, video_title: str):
    print("=" * 70)
    print(f"[*] MENJALANKAN ENJIN TYPESAFE AI JEV SYSTEM ONE PADA VIDEO:")
    print(f"    Tajuk: {video_title}")
    print("=" * 70)

    # Initialize Jev client
    client = TypeSafeClient(mode="auto")
    engine_name = "JevCloudAdapter" if client.cloud_adapter else "NonAutoregressiveLocalEngine"
    print(f"[+] Jev Client Mode: {client.mode}")
    print(f"[+] Jev Active Engine: {engine_name}")

    # Define Jev primitives
    topic_choice = Choice(
        options=[
            "RESEPI_RAMADAN",
            "RESEPI_VIRAL_HARIAN",
            "TRAVELOG_VLOG",
            "BEHIND_THE_SCENES_BISNES",
            "COMMUNITY_CSR"
        ],
        instructions="Klasifikasikan kategori topik kandungan video TikTok ini berdasarkan transkrip."
    )

    hook_choice = Choice(
        options=[
            "CRAVING_SENSORY",
            "SIGNATURE_GREETING",
            "STORY_CURIOSITY",
            "DIRECT_VALUE",
            "EMPATHY_RELATABLE"
        ],
        instructions="Kenal pasti jenis hook pembuka (3-5 saat pertama) yang digunakan oleh pencipta kandungan."
    )

    pacing_choice = Choice(
        options=[
            "RAPID_FIRE",
            "MODERATE_RHYTHMIC",
            "NARRATIVE_SLOW"
        ],
        instructions="Tentukan rentak kelajuan suntingan dan lontaran suara berdasarkan kepadatan ayat."
    )

    virality_score = Score(
        min=1,
        max=10,
        instructions="Nilaikan skor potensi viraliti (1-10) berdasarkan kekuatan hook dan emosi audiens."
    )

    catchphrase_gate = Noul(
        instructions="Adakah video ini mengandungi frasa ikonik jenama seperti 'Hey what's up guys' atau 'terangkat habis'?",
        threshold=0.5
    )

    # Process through Jev System One
    t0 = time.perf_counter()
    resp = client.system_one(
        state={
            "title": video_title,
            "transcript": transcript
        },
        questions={
            "topic": topic_choice,
            "hook_type": hook_choice,
            "pacing": pacing_choice,
            "viral_score": virality_score,
            "has_catchphrase": catchphrase_gate
        }
    )
    duration_ms = (time.perf_counter() - t0) * 1000

    print(f"\n[+] KEPUTUSAN JEV SYSTEM ONE SELESAI DALAM: {resp.latency_ms:.2f} ms (Total Wall: {duration_ms:.2f} ms)")
    print("-" * 70)

    topic_ans = resp.answers["topic"]
    print(f"1. TOPIC CATEGORY: {topic_ans.value}")
    print(f"   Confidence: {topic_ans.confidence:.4f} | Entropy: {topic_ans.entropy:.4f}")
    print(f"   Taburan Kebarangkalian:")
    for opt, prob in topic_ans.probabilities.items():
        bar = "#" * int(prob * 30)
        print(f"     - {opt:<24}: {prob*100:5.1f}% | {bar}")

    print("-" * 70)
    hook_ans = resp.answers["hook_type"]
    print(f"2. HOOK TYPE: {hook_ans.value}")
    print(f"   Confidence: {hook_ans.confidence:.4f} | Entropy: {hook_ans.entropy:.4f}")
    print(f"   Taburan Kebarangkalian:")
    for opt, prob in hook_ans.probabilities.items():
        bar = "#" * int(prob * 30)
        print(f"     - {opt:<24}: {prob*100:5.1f}% | {bar}")

    print("-" * 70)
    pacing_ans = resp.answers["pacing"]
    print(f"3. PACING SPEED: {pacing_ans.value} (Confidence: {pacing_ans.confidence:.4f})")

    print("-" * 70)
    score_ans = resp.answers["viral_score"]
    print(f"4. ESTIMATED VIRAL SCORE: {score_ans.value}/10 (Expected: {score_ans.expected_value:.2f}/10)")

    print("-" * 70)
    gate_ans = resp.answers["has_catchphrase"]
    print(f"5. SIGNATURE CATCHPHRASE GATE: {'YA (TRUE)' if gate_ans.is_true else 'TIDAK (FALSE)'} (Prob: {gate_ans.value:.4f})")
    print("=" * 70)

    return {
        "topic": topic_ans.value,
        "hook_type": hook_ans.value,
        "pacing": pacing_ans.value,
        "viral_score": score_ans.value,
        "has_catchphrase": gate_ans.is_true,
        "latency_ms": resp.latency_ms
    }

if __name__ == "__main__":
    sample_transcript = (
        "Hey what's up guys! Hari ini kita start Episod 1 daripada 30 Hari 30 Resepi untuk Ramadan tahun ni, "
        "and resipi pertama kita ialah Daging Masak Hitam Berempah yang sangat pekat, juicy dan pecah minyak elok. "
        "First sekali kita ambil daging lembu yang dipotong nipis, perap dengan kicap manis, kicap pekat dan sedikit sos tiram selama 30 minit. "
        "Kemudian kita kisar bawang merah, bawang putih, halia, serai dan cili kering sampai lumat. "
        "Bila dicedok atas nasi panas berasap, bismillah... rasa rempah dia meresap sampai ke dalam, daging lembut tak liat langsung, memang terangkat habis!"
    )
    analyze_with_jev(sample_transcript, "Episod 1: Daging Masak Hitam Berempah")
