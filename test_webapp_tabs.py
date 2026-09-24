from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 850})
    page.goto("http://127.0.0.1:8765")
    page.wait_for_timeout(1000)

    # 1. Click Tab Scorer
    page.click("#tab-btn-scorer")
    page.wait_for_timeout(500)
    # Click preset 1
    page.click("button:has-text('Ayam Crispy')")
    page.wait_for_timeout(300)
    # Click Score button
    page.click("#scoreBtn")
    page.wait_for_timeout(1500)
    page.screenshot(path=r"C:\Users\User\projects\web-computer-use\screenshots\webapp_scorer.png")
    print("[+] Scorer tab tested and screenshot saved!")

    # 2. Click Tab Generator
    page.click("#tab-btn-generator")
    page.wait_for_timeout(500)
    # Fill product
    page.fill("#genProduct", "Sambal Dendeng Paru Berapi")
    # Click Generate
    page.click("#generateBtn")
    page.wait_for_timeout(1500)
    page.screenshot(path=r"C:\Users\User\projects\web-computer-use\screenshots\webapp_generator.png")
    print("[+] Generator tab tested and screenshot saved!")

    browser.close()
