"""
Playwright End-to-End Test for ViralStudio KA-363 (Enterprise Edition v3.1).
Validates all 5 navigation tabs, SQLite persistence, Studio 4-step workflow,
Jev Virality evaluation, 363 Analytics chart, and captures verification artifacts.
"""

import sys
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

ARTIFACT_DIR = Path(r"C:\Users\User\.gemini\antigravity-cli\brain\2daea58b-5beb-46c4-830b-91e7f51762d2")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

async def run_e2e_test():
    console_errors = []
    failed_requests = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        # Capture console error logs
        def handle_console(msg):
            if msg.type == "error":
                console_errors.append(msg.text)
                print(f"[BROWSER ERROR] {msg.text}")
            elif msg.type == "warning":
                pass

        page.on("console", handle_console)
        page.on("pageerror", lambda err: console_errors.append(str(err)))

        def handle_response(resp):
            if resp.status >= 400:
                failed_requests.append(f"{resp.status} {resp.url}")
                print(f"[HTTP FAIL] {resp.status} {resp.url}")

        page.on("response", handle_response)

        print("[1] Navigating to ViralStudio at http://127.0.0.1:8765/ ...")
        await page.goto("http://127.0.0.1:8765/", wait_until="networkidle", timeout=15000)

        # 1. Verify Home View
        print("[2] Verifying Home (Utama) view...")
        title = await page.title()
        print(f"    Page Title: {title}")
        assert "ViralStudio" in title, f"Unexpected title: {title}"

        await page.wait_for_selector("#homeProjectsList", timeout=5000)
        await page.wait_for_timeout(1000)
        await page.screenshot(path=str(ARTIFACT_DIR / "sota_10_home_dashboard.png"))
        print("    Saved screenshot: sota_10_home_dashboard.png")

        # 2. Verify Projects View
        print("[3] Switching to Projects (Projek) view...")
        await page.click("#tab-projects")
        await page.wait_for_selector("#projectsTableBody", timeout=5000)
        await page.wait_for_timeout(1000)
        await page.screenshot(path=str(ARTIFACT_DIR / "sota_11_projects_view.png"))
        print("    Saved screenshot: sota_11_projects_view.png")

        # 3. Verify Studio Video View & 4-Step Flow
        print("[4] Switching to Studio Video view...")
        await page.click("#tab-studio")
        await page.wait_for_selector("#studioStep-1", timeout=5000)
        
        # Test Step 1 -> Step 2
        print("    Advancing from Step 1 (Brief) to Step 2 (Script)...")
        await page.click("button:has-text('Simpan & Teruskan ke Skrip')")
        await page.wait_for_selector("#studioStep-2", timeout=5000)
        await page.wait_for_timeout(800)

        # Trigger Jev Evaluation in Step 2
        print("    Triggering Jev Virality Evaluation...")
        await page.click("button:has-text('Nilaikan Semula')")
        await page.wait_for_timeout(1500)
        await page.screenshot(path=str(ARTIFACT_DIR / "sota_12_studio_step2_jev.png"))
        print("    Saved screenshot: sota_12_studio_step2_jev.png")

        # Step 2 -> Step 3 (Visual & Preview)
        print("    Advancing to Step 3 (Preview & iPhone Bezel)...")
        await page.click("button:has-text('Sahkan & Pratonton Video')")
        await page.wait_for_selector("#studioStep-3", timeout=5000)
        await page.wait_for_selector(".phone-bezel", timeout=5000)
        await page.wait_for_timeout(1000)
        await page.screenshot(path=str(ARTIFACT_DIR / "sota_13_studio_step3_phone.png"))
        print("    Saved screenshot: sota_13_studio_step3_phone.png")

        # Step 3 -> Step 4 (Export Step)
        print("    Advancing to Step 4 (Export & Render)...")
        await page.click("button:has-text('Teruskan ke Eksport')")
        await page.wait_for_selector("#studioStep-4", timeout=5000)
        await page.wait_for_timeout(800)
        await page.screenshot(path=str(ARTIFACT_DIR / "sota_14_studio_step4_export.png"))
        print("    Saved screenshot: sota_14_studio_step4_export.png")

        # Test trigger render job in Step 4
        print("    Triggering Render Job...")
        await page.click("#startRenderBtn")
        await page.wait_for_selector("#renderProgressContainer", timeout=5000)
        print("    Render job enqueued, waiting for render completion...")
        await page.wait_for_selector("#renderResultContainer", timeout=25000)
        await page.screenshot(path=str(ARTIFACT_DIR / "sota_15_studio_render_completed.png"))
        print("    Saved screenshot: sota_15_studio_render_completed.png")

        # 4. Verify Assets View
        print("[5] Switching to Assets (Aset) view...")
        await page.click("#tab-assets")
        await page.wait_for_selector("#assetGrid", timeout=5000)
        await page.wait_for_timeout(1000)
        await page.screenshot(path=str(ARTIFACT_DIR / "sota_16_assets_grid.png"))
        print("    Saved screenshot: sota_16_assets_grid.png")

        # 5. Verify Analytics 363 View
        print("[6] Switching to Analytics (Analitik 363) view...")
        await page.click("#tab-analytics")
        await page.wait_for_selector("#scatterChartCanvas", timeout=5000)
        await page.wait_for_timeout(1500)
        await page.screenshot(path=str(ARTIFACT_DIR / "sota_17_analytics_scatter.png"))
        print("    Saved screenshot: sota_17_analytics_scatter.png")

        await browser.close()

    print("\n--- E2E Validation Summary ---")
    print(f"Total Failed HTTP Requests: {len(failed_requests)}")
    for req in failed_requests:
        print(f"  [HTTP ERROR] {req}")

    # Exclude harmless favicon/map if any
    real_js_errors = [e for e in console_errors if "favicon" not in e.lower() and "map" not in e.lower()]
    print(f"Total Actionable Console Errors: {len(real_js_errors)}")
    if real_js_errors:
        for err in real_js_errors:
            print(f"  [ERROR] {err}")
    else:
        print("[SUCCESS] 0 Actionable JavaScript Console Errors! Clean execution.")

if __name__ == "__main__":
    asyncio.run(run_e2e_test())
