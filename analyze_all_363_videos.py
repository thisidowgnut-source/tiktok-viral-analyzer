"""
Batch Analyzer for ALL 363 Khairul Aming TikTok Videos.
Categorizes every video via TypeSafe AI Jev System One primitives, computes engagement metrics,
identifies top viral formulas, and outputs full master JSON and Google Sheets CSV.
"""

import sys
import json
import time
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Add typesafe-system-one
sys.path.insert(0, r"C:\Users\User\projects\typesafe-system-one")
from core import TypeSafeClient, Choice, Score, Noul

INPUT_CATALOG = r"C:\Users\User\projects\tiktok-viral-analyzer\khairulaming_all_videos_catalog.json"
OUTPUT_JSON = r"C:\Users\User\projects\tiktok-viral-analyzer\khairulaming_all_363_analysis.json"
OUTPUT_CSV = r"C:\Users\User\projects\tiktok-viral-analyzer\khairulaming_all_363_analysis.csv"

def run_full_analysis():
    print("=" * 72)
    print("  MEMPROSES KESELURUHAN 363 VIDEO TIKTOK @KHAIRULAMING MELALUI JEV      ")
    print("=" * 72)

    with open(INPUT_CATALOG, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    print(f"[+] Jumlah video dalam katalog: {len(catalog)}")

    client = TypeSafeClient(mode="local") # Use ultra-fast local engine for 363 videos in 5 seconds!
    print(f"[+] Menggunakan Enjin Pantas TypeSafe Jev System One (Non-Autoregressive)...")

    topic_choice = Choice(
        options=[
            "RESEPI_RAMADAN",
            "RESEPI_VIRAL_HARIAN",
            "TRAVELOG_VLOG",
            "BEHIND_THE_SCENES_BISNES",
            "COMMUNITY_CSR"
        ],
        instructions="Klasifikasikan kategori topik kandungan video TikTok ini berdasarkan tajuk dan huraian."
    )

    hook_choice = Choice(
        options=[
            "CRAVING_SENSORY",
            "SIGNATURE_GREETING",
            "STORY_CURIOSITY",
            "DIRECT_VALUE",
            "EMPATHY_RELATABLE"
        ],
        instructions="Kenal pasti jenis hook pembuka berdasarkan gaya penulisan dan mesej video."
    )

    pacing_choice = Choice(
        options=[
            "RAPID_FIRE",
            "MODERATE_RHYTHMIC",
            "NARRATIVE_SLOW"
        ],
        instructions="Tentukan kepantasan rentak video berdasarkan durasi saat dan kepadatan kapsyen."
    )

    processed = []
    category_counts = {}
    hook_counts = {}
    total_views = 0
    total_likes = 0
    total_shares = 0

    t_start = time.perf_counter()

    for idx, item in enumerate(catalog, 1):
        vid_id = item["video_id"]
        title = item.get("title", "")
        views = item.get("views", 0)
        likes = item.get("likes", 0)
        shares = item.get("shares", 0)
        comments = item.get("comments", 0)
        saves = item.get("saves", 0)
        duration = item.get("duration_sec", 60)

        total_views += views
        total_likes += likes
        total_shares += shares

        # Process with Jev
        resp = client.system_one(
            state={
                "title": title,
                "duration": duration,
                "views": views
            },
            questions={
                "topic": topic_choice,
                "hook": hook_choice,
                "pacing": pacing_choice
            }
        )

        topic = resp.answers["topic"].value
        hook = resp.answers["hook"].value
        pacing = resp.answers["pacing"].value

        category_counts[topic] = category_counts.get(topic, 0) + 1
        hook_counts[hook] = hook_counts.get(hook, 0) + 1

        # Engagement Rate = (Likes + Comments + Shares*3 + Saves*2) / Views
        eng_rate = round(((likes + comments + (shares * 3) + (saves * 2)) / (views if views > 0 else 1)) * 100, 2)

        processed.append({
            "order": idx,
            "video_id": vid_id,
            "title": title,
            "url": item.get("url", f"https://www.tiktok.com/@khairulaming/video/{vid_id}"),
            "topic_category": topic,
            "hook_type": hook,
            "pacing_speed": pacing,
            "duration_sec": duration,
            "views": views,
            "likes": likes,
            "shares": shares,
            "comments": comments,
            "saves": saves,
            "engagement_rate_pct": eng_rate,
            "jev_latency_ms": resp.latency_ms
        })

    total_time = (time.perf_counter() - t_start) * 1000

    # Save to JSON
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(processed, f, ensure_ascii=False, indent=2)

    # Save to CSV
    with open(OUTPUT_CSV, "w", encoding="utf-8") as f:
        f.write("order,video_id,topic_category,hook_type,pacing_speed,duration_sec,views,likes,shares,comments,saves,engagement_rate_pct,title,url\n")
        for p in processed:
            def clean(txt):
                return '"' + str(txt).replace('"', '""') + '"'
            row = [
                str(p["order"]),
                clean(p["video_id"]),
                clean(p["topic_category"]),
                clean(p["hook_type"]),
                clean(p["pacing_speed"]),
                str(p["duration_sec"]),
                str(p["views"]),
                str(p["likes"]),
                str(p["shares"]),
                str(p["comments"]),
                str(p["saves"]),
                str(p["engagement_rate_pct"]),
                clean(p["title"]),
                clean(p["url"])
            ]
            f.write(",".join(row) + "\n")

    print(f"\n[+] SELESAI MEMPROSES KESEMUA {len(processed)} VIDEO DALAM {total_time:.2f} MS!")
    print(f"[+] Purata Latensi Jev per video: {total_time / len(processed):.3f} ms")
    print(f"\n--- STATISTIK KESELURUHAN AKAUN KHAIRUL AMING ---")
    print(f"  * Jumlah Video Dituai : {len(processed)}")
    print(f"  * Jumlah Tontonan     : {total_views:,} tontonan ({total_views / 1e9:.2f} Bilion views!)")
    print(f"  * Jumlah Suka (Likes) : {total_likes:,}")
    print(f"  * Jumlah Perkongsian  : {total_shares:,}")
    print(f"\n--- TABURAN KATEGORI KANDUNGAN ---")
    for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {cat:<26}: {count:3d} video ({count/len(processed)*100:.1f}%)")

    print(f"\n--- TABURAN JENIS HOOK ---")
    for hk, count in sorted(hook_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {hk:<26}: {count:3d} video ({count/len(processed)*100:.1f}%)")

    # Top 5 Most Viewed Videos
    top_5 = sorted(processed, key=lambda x: x["views"], reverse=True)[:5]
    print(f"\n--- TOP 5 VIDEO PALING VIRAL SEPANJANG ZAMAN ---")
    for i, v in enumerate(top_5, 1):
        print(f"  {i}. [{v['views']:,} views] {v['topic_category']} | {v['title'][:60]}")

    print(f"\n[+] Output JSON: {OUTPUT_JSON}")
    print(f"[+] Output CSV:  {OUTPUT_CSV}")
    print("=" * 72)

if __name__ == "__main__":
    run_full_analysis()
