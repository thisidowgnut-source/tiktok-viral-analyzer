"""
Extract live TikTok videos and metadata from @khairulaming using Playwright headless browser.
"""

import json
import time
from playwright.sync_api import sync_playwright
from pathlib import Path

def extract_khairulaming_videos():
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 900}
        )
        page = context.new_page()
        print("[*] Melayari https://www.tiktok.com/@khairulaming...")
        page.goto("https://www.tiktok.com/@khairulaming", wait_until="networkidle", timeout=30000)
        time.sleep(3)

        # Scrape video cards
        # Look for anchor tags pointing to video
        video_links = page.query_selector_all("a[href*='/video/']")
        print(f"[+] Ditemui {len(video_links)} pautan video!")

        seen_urls = set()
        for link in video_links:
            href = link.get_attribute("href")
            if not href or href in seen_urls:
                continue
            seen_urls.add(href)

            # Try to get views count
            views_text = ""
            card = link.query_selector("xpath=..")
            if card:
                views_el = card.query_selector("[data-e2e='video-views']") or card.query_selector("strong")
                if views_el:
                    views_text = views_el.inner_text()

            # Try to get title or img alt
            img = link.query_selector("img")
            alt_text = img.get_attribute("alt") if img else ""

            results.append({
                "video_url": href if href.startswith("http") else f"https://www.tiktok.com{href}",
                "views_display": views_text,
                "alt_desc": alt_text
            })

            if len(results) >= 6:
                break

        browser.close()

    output_file = Path("live_khairulaming_scraped.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"[+] Disimpan {len(results)} video ke {output_file.resolve()}")
    return results

if __name__ == "__main__":
    extract_khairulaming_videos()
