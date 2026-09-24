from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1400, "height": 950})
    page.goto("http://127.0.0.1:8765")
    page.wait_for_timeout(1000)

    # 1. Capture 363 Hub with new Quick Filter Pills
    page.screenshot(path=r"C:\Users\User\projects\web-computer-use\screenshots\webapp_enhanced_hub.png")
    print("[+] Enhanced 363 Hub screenshot saved")

    # 2. Switch to DOH-NUT tab
    page.click("#tab-btn-dohnut")
    page.wait_for_timeout(800)
    page.screenshot(path=r"C:\Users\User\projects\web-computer-use\screenshots\webapp_enhanced_dohnut.png")
    print("[+] Enhanced DOH-NUT & Social Command screenshot saved")

    # 3. Open 31-Flavor Catalog Modal
    page.click("button:has-text('Buka Katalog 31 Perisa')")
    page.wait_for_timeout(800)
    page.screenshot(path=r"C:\Users\User\projects\web-computer-use\screenshots\webapp_catalog_modal.png")
    print("[+] 31-Flavor Catalog Modal screenshot saved")
    page.click("#catalogModal button:has-text('✕')")
    page.wait_for_timeout(300)

    # 4. Open Command Palette (Ctrl+K)
    page.keyboard.press("Control+k")
    page.wait_for_timeout(500)
    page.screenshot(path=r"C:\Users\User\projects\web-computer-use\screenshots\webapp_command_palette.png")
    print("[+] Command Palette screenshot saved")

    browser.close()
