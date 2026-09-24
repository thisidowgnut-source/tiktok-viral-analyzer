"""
Full TikTok Profile Harvester for @khairulaming.
Intercepts TikTok internal JSON feed API (/api/post/item_list/) while auto-scrolling
to harvest ALL videos with exact metadata (views, likes, shares, comments, createTime, desc, video_url).
"""

import os
import sys
import json
import time
from playwright.sync_api import sync_playwright
from pathlib import Path

CHROME_PROFILE = r"C:\Users\User\projects\web-computer-use\agent_chrome_profile"
OUTPUT_FILE = r"C:\Users\User\projects\tiktok-viral-analyzer\khairulaming_all_videos_raw.json"
SUMMARY_FILE = r"C:\Users\User\projects\tiktok-viral-analyzer\khairulaming_all_videos_catalog.json"

all_videos = {}

def handle_response(response):
    # Intercept TikTok post item_list API
    if "/api/post/item_list" in response.url or "item_list" in response.url:
        try:
            data = response.json()
            items = data.get("itemList") or data.get("items") or []
            print(f"[+] API Intercepted: {len(items)} items received from network!")
            for item in items:
                vid_id = item.get("id")
                if not vid_id or vid_id in all_videos:
                    continue
                stats = item.get("stats") or {}
                desc = item.get("desc") or ""
                create_time = item.get("createTime")
                video_info = item.get("video") or {}
                duration = video_info.get("duration", 0)

                all_videos[vid_id] = {
                    "video_id": vid_id,
                    "title": desc,
                    "url": f"https://www.tiktok.com/@khairulaming/video/{vid_id}",
                    "views": stats.get("playCount", 0),
                    "likes": stats.get("diggCount", 0),
                    "shares": stats.get("shareCount", 0),
                    "comments": stats.get("commentCount", 0),
                    "saves": stats.get("collectCount", 0),
                    "duration_sec": duration,
                    "create_time": create_time
                }
            print(f"    Total videos collected so far: {len(all_videos)}")
        except Exception as e:
            pass

def harvest_all_videos():
    print("=" * 70)
    print("[*] MEMULAKAN PENUAIAN PENUH SEMUA VIDEO TIKTOK @KHAIRULAMING")
    print("=" * 70)

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            user_data_dir=CHROME_PROFILE,
            channel="chrome",
            headless=True,
            viewport={"width": 1366, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.on("response", handle_response)

        print("[*] Melayari profil https://www.tiktok.com/@khairulaming...")
        try:
            page.goto("https://www.tiktok.com/@khairulaming", wait_until="domcontentloaded", timeout=45000)
            time.sleep(5)
        except Exception as e:
            print(f"[-] Ralat muat turun: {e}")

        # Extract videos currently in DOM as well
        dom_videos = page.evaluate("""() => {
            const list = [];
            const links = document.querySelectorAll('a[href*="/video/"]');
            for (let a of links) {
                const href = a.href;
                const m = href.match(/\\/video\\/(\\d+)/);
                if (m) {
                    const img = a.querySelector('img');
                    const alt = img ? img.alt : '';
                    let views = '';
                    const parent = a.closest('[data-e2e*="item"]') || a.parentElement;
                    if (parent) {
                        const vEl = parent.querySelector('[data-e2e="video-views"]') || parent.querySelector('strong');
                        if (vEl) views = vEl.innerText;
                    }
                    list.push({ id: m[1], url: href, title: alt, views_text: views });
                }
            }
            return list;
        }""")
        print(f"[+] Video dikesan di DOM awal: {len(dom_videos)}")
        for dv in dom_videos:
            if dv["id"] not in all_videos:
                all_videos[dv["id"]] = {
                    "video_id": dv["id"],
                    "title": dv["title"],
                    "url": dv["url"],
                    "views_display": dv["views_text"]
                }

        # Auto-scroll loop to load ALL videos
        print("[*] Mula skrol berulang untuk memuat turun kesemua video...")
        last_count = len(all_videos)
        no_new_cycles = 0

        for scroll_i in range(1, 40):  # Up to 40 scrolls (each loads ~30 videos)
            page.evaluate("window.scrollBy(0, 1500)")
            time.sleep(2.5)

            # Check DOM again
            more_dom = page.evaluate("""() => {
                const list = [];
                const links = document.querySelectorAll('a[href*="/video/"]');
                for (let a of links) {
                    const href = a.href;
                    const m = href.match(/\\/video\\/(\\d+)/);
                    if (m) {
                        const img = a.querySelector('img');
                        const alt = img ? img.alt : '';
                        let views = '';
                        const parent = a.closest('[data-e2e*="item"]') || a.parentElement;
                        if (parent) {
                            const vEl = parent.querySelector('[data-e2e="video-views"]') || parent.querySelector('strong');
                            if (vEl) views = vEl.innerText;
                        }
                        list.push({ id: m[1], url: href, title: alt, views_text: views });
                    }
                }
                return list;
            }""")

            for dv in more_dom:
                if dv["id"] not in all_videos:
                    all_videos[dv["id"]] = {
                        "video_id": dv["id"],
                        "title": dv["title"],
                        "url": dv["url"],
                        "views_display": dv["views_text"]
                    }

            current_count = len(all_videos)
            print(f"  [Skrol #{scroll_i}] Jumlah video terkumpul: {current_count}")

            if current_count == last_count:
                no_new_cycles += 1
                if no_new_cycles >= 4:
                    print("[+] Tiada lagi video baharu dimuat turun (hujung halaman dicapai).")
                    break
            else:
                no_new_cycles = 0
                last_count = current_count

        ctx.close()

    # Save all videos
    video_list = list(all_videos.values())
    with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
        json.dump(video_list, f, ensure_ascii=False, indent=2)

    print("=" * 70)
    print(f"[+] SELESAI PENUAIAN! Berjaya mengumpul {len(video_list)} video Khairul Aming.")
    print(f"[+] Disimpan ke: {SUMMARY_FILE}")
    print("=" * 70)
    return video_list

if __name__ == "__main__":
    harvest_all_videos()
