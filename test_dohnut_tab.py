from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1400, "height": 900})
    page.goto("http://127.0.0.1:8765")
    page.wait_for_timeout(1000)

    # Click Tab Doh-Nut
    page.click("#tab-btn-dohnut")
    page.wait_for_timeout(1000)
    page.screenshot(path=r"C:\Users\User\projects\web-computer-use\screenshots\webapp_dohnut_ground_truth.png")
    print("[+] Doh-Nut tab screenshot saved to webapp_dohnut_ground_truth.png")

    browser.close()
