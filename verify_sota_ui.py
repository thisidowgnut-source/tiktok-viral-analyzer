import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright

SCREENSHOTS_DIR = Path(r"C:\Users\User\projects\web-computer-use\screenshots")
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

ARTIFACTS_DIR = Path(r"C:\Users\User\.gemini\antigravity-cli\brain\2daea58b-5beb-46c4-830b-91e7f51762d2")

async def run_verification():
    console_errors = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 960})
        page = await context.new_page()

        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda err: console_errors.append(str(err)))

        print("[1] Navigating to http://127.0.0.1:8765...")
        await page.goto("http://127.0.0.1:8765", wait_until="networkidle")
        await asyncio.sleep(1)

        # 1. Capture Hub Tab
        hub_path = SCREENSHOTS_DIR / "sota_01_hub.png"
        await page.screenshot(path=str(hub_path), full_page=False)
        print(f"[*] Hub screenshot saved: {hub_path}")

        # 2. Switch to Doh-Nut Tab (Three.js 3D WebGL Donut & Campaign Cards)
        print("[2] Switching to Doh-Nut tab...")
        await page.click("#tab-btn-dohnut")
        await asyncio.sleep(2)  # Wait for Three.js render loop

        dohnut_path = SCREENSHOTS_DIR / "sota_02_dohnut_3d_showcase.png"
        await page.screenshot(path=str(dohnut_path), full_page=False)
        print(f"[*] Doh-Nut 3D Showcase screenshot saved: {dohnut_path}")

        # 3. Open 31-Flavor Catalog Modal
        print("[3] Opening 31-Flavor Catalog Modal...")
        await page.click("button:has-text('Buka Katalog 31 Perisa')")
        await asyncio.sleep(1.5)

        catalog_path = SCREENSHOTS_DIR / "sota_03_31_flavors_catalog.png"
        await page.screenshot(path=str(catalog_path), full_page=False)
        print(f"[*] Catalog Modal screenshot saved: {catalog_path}")

        # Close Modal
        await page.keyboard.press("Escape")
        await asyncio.sleep(0.5)

        # 4. Switch to Jev Scorer Tab & Run Automotive Speedometer
        print("[4] Testing Jev Scorer with Speedometer...")
        await page.click("#tab-btn-scorer")
        await asyncio.sleep(0.5)
        # Click Preset 1 inside #tab-scorer
        await page.click("#tab-scorer button:has-text('Doh-Nut Salted Egg')")
        await asyncio.sleep(0.5)
        # Click Score Button
        await page.click("#scoreBtn")
        await asyncio.sleep(2.0)  # Wait for needle transition and bar fills

        scorer_path = SCREENSHOTS_DIR / "sota_04_speedometer_gauge.png"
        await page.screenshot(path=str(scorer_path), full_page=False)
        print(f"[*] Speedometer Gauge screenshot saved: {scorer_path}")

        # 5. Switch to Script Studio & Live iPhone 16 Pro Mockup
        print("[5] Testing Script Studio & iPhone 16 Pro Mockup...")
        await page.click("#tab-btn-generator")
        await asyncio.sleep(0.5)
        # Click Generate Button
        await page.click("#generateBtn")
        await asyncio.sleep(2.0)

        # Switch to Phase 2 to test interactivity
        phase2_btn = page.locator("#phase-card-2")
        if await phase2_btn.count() > 0:
            await phase2_btn.click()
            await asyncio.sleep(1)

        studio_path = SCREENSHOTS_DIR / "sota_05_iphone_mockup_studio.png"
        await page.screenshot(path=str(studio_path), full_page=False)
        print(f"[*] iPhone Studio screenshot saved: {studio_path}")

        await browser.close()

    print("\n--- Console Errors Check ---")
    if console_errors:
        print(f"[!] Encountered {len(console_errors)} console errors:")
        for err in console_errors:
            print("   -", err)
    else:
        print("[OK] Clean console! 0 JavaScript errors.")

    # Copy screenshots to artifact directory for presentation
    import shutil
    for sp in [dohnut_path, catalog_path, scorer_path, studio_path]:
        if sp.exists():
            shutil.copy2(sp, ARTIFACTS_DIR / sp.name)
            print(f"[+] Copied {sp.name} to brain artifacts.")

if __name__ == "__main__":
    asyncio.run(run_verification())
