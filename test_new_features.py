from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    page.goto("http://127.0.0.1:8765")
    page.wait_for_timeout(1000)

    # 1. Capture Doh-Nut Showcase
    page.click("#tab-btn-dohnut")
    page.wait_for_timeout(600)
    page.screenshot(path=r"C:\Users\User\projects\web-computer-use\screenshots\webapp_dohnut.png")
    print("[+] webapp_dohnut.png captured!")

    # 2. Capture A2A Multi-Agent Arena
    page.click("#tab-btn-a2a")
    page.wait_for_timeout(400)
    page.click("#a2aRunBtn")
    page.wait_for_timeout(2000)
    page.screenshot(path=r"C:\Users\User\projects\web-computer-use\screenshots\webapp_a2a.png")
    print("[+] webapp_a2a.png captured!")

    # 3. Capture Floating Copilot
    page.click("#copilotTrigger")
    page.wait_for_timeout(400)
    page.fill("#copilotInput", "Kenapa jenama Doh-Nut begitu viral?")
    page.keyboard.press("Enter")
    page.wait_for_timeout(1000)
    page.screenshot(path=r"C:\Users\User\projects\web-computer-use\screenshots\webapp_copilot.png")
    print("[+] webapp_copilot.png captured!")

    browser.close()
