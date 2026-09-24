"""
Scrape live TikTok videos from @khairulaming using real Chrome channel persistent context.
"""

import os
import sys
import json
import time
from playwright.sync_api import sync_playwright

CHROME_PROFILE = r"C:\Users\User\projects\web-computer-use\agent_chrome_profile"
OUTPUT_FILE = r"C:\Users\User\projects\tiktok-viral-analyzer\khairulaming_live_scraped.json"

def scrape():
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            user_data_dir=CHROME_PROFILE,
            channel="chrome",
            headless=True,
            viewport={"width": 1366, "height": 850},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        print("[*] Melayari TikTok @khairulaming...")
        page.goto("https://www.tiktok.com/@khairulaming", wait_until="domcontentloaded", timeout=45000)
        time.sleep(4)

        # Scroll down slightly to trigger video card hydration
        page.evaluate("window.scrollBy(0, 500)")
        time.sleep(3)

        # Extract videos
        videos = page.evaluate("""() => {
            const items = [];
            // Target all video cards
            const links = document.querySelectorAll('a[href*="/video/"]');
            for (let a of links) {
                const href = a.href;
                const img = a.querySelector('img');
                const alt = img ? img.alt : '';
                
                // Find view count in ancestor or sibling
                let views = '';
                let parent = a.closest('[data-e2e*="item"]') || a.parentElement;
                if (parent) {
                    const viewsEl = parent.querySelector('[data-e2e="video-views"]') || parent.querySelector('strong');
                    if (viewsEl) views = viewsEl.innerText;
                }
                
                items.push({
                    url: href,
                    title: alt || 'Video Khairul Aming',
                    views: views
                });
            }
            return items;
        }""")

        print(f"[+] Berjaya mengekstrak {len(videos)} video langsung!")
        for idx, v in enumerate(videos[:5], 1):
            print(f"  {idx}. {v['title'][:60]} | Views: {v['views']} | URL: {v['url']}")

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(videos, f, ensure_ascii=False, indent=2)

        ctx.close()

if __name__ == "__main__":
    scrape()
