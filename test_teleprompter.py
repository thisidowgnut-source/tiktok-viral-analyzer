from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    page.goto("http://127.0.0.1:8765")
    page.wait_for_timeout(1000)

    # 1. Switch to Doh-Nut tab
    page.click("#tab-btn-dohnut")
    page.wait_for_timeout(500)

    # 2. Click "Buka Teleprompter" on the first campaign (ASMR Lava)
    page.click("button:has-text('Buka Teleprompter')")
    page.wait_for_timeout(800)

    # 3. Take screenshot of Live Teleprompter Studio
    page.screenshot(path=r"C:\Users\User\projects\web-computer-use\screenshots\webapp_teleprompter.png")
    print("[+] webapp_teleprompter.png captured successfully!")

    # 4. Test Play Prompter
    page.click("#prompterPlayBtn")
    page.wait_for_timeout(1000)
    print("[+] Prompter play tested!")

    browser.close()
