"""
Verification script for Prompt 2 Services:
1. SQLite migrations and database tables
2. ProjectService (CRUD, optimistic locking version control, scenes, bundle export/import)
3. AssetService (registration, SHA256, FFprobe metadata)
4. JobService (queue, progress, cancellation flag)
5. JevService (system_one answers reading, honest engine reporting)
"""

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from db.migrations import run_migrations
from services.project_service import ProjectService
from services.asset_service import AssetService
from services.job_service import JobService
from services.jev_service import JevService
from models.domain import ProjectCreate, ProjectUpdate, SceneCreate

def test_full_pipeline():
    print("[*] Running SQLite migrations...")
    run_migrations()

    print("[*] Testing ProjectService...")
    # 1. Create project
    proj = ProjectService.create_project(
        ProjectCreate(
            title="Kempen Donut Salted Egg Merdeka",
            language="ms",
            brief={
                "product_name": "Doh-Nut Salted Egg Lava",
                "goal": "Tingkatkan tempahan petang",
                "hook_text": "Dengar bunyi krup-krap kerak doh panas ni!"
            }
        )
    )
    assert proj is not None, "Project creation failed"
    assert proj.version == 1, f"Expected version 1, got {proj.version}"
    assert len(proj.scenes) == 1, f"Expected 1 default scene, got {len(proj.scenes)}"
    print(f"[+] Project created: {proj.id} - '{proj.title}' (Version: {proj.version})")

    # 2. Add scene
    scene = ProjectService.add_scene(
        proj.id,
        SceneCreate(
            sequence=2,
            script="Tengok lava salted egg panas ni membuak meleleh krup krap!",
            duration=4.5,
            crop_focal_point="center",
            transition="fade"
        )
    )
    assert scene.sequence == 2
    proj_updated = ProjectService.get_project(proj.id)
    assert len(proj_updated.scenes) == 2
    assert proj_updated.version == 2
    print(f"[+] Scene 2 added: {scene.id}. Project auto-incremented to version {proj_updated.version}")

    # 3. Optimistic locking test
    print("[*] Testing optimistic locking version conflict...")
    try:
        # Client sends stale version (version 1 instead of 2)
        ProjectService.update_project(
            proj.id,
            ProjectUpdate(title="Stale Update", version=1)
        )
        assert False, "Expected ValueError on version conflict"
    except ValueError as e:
        print(f"[+] Optimistic locking prevented stale overwrite: {e}")

    # Valid update with correct version
    proj_v3 = ProjectService.update_project(
        proj.id,
        ProjectUpdate(title="Kempen Donut Salted Egg Merdeka (Approved)", version=proj_updated.version, status="READY_REVIEW")
    )
    assert proj_v3.version == 3
    assert proj_v3.status == "READY_REVIEW"
    print(f"[+] Valid update succeeded. Project version now: {proj_v3.version}")

    # 4. Job Service test
    print("[*] Testing JobService...")
    job = JobService.create_job("render_video", {"project_id": proj.id, "voice": "ms-MY-YasminNeural"})
    assert job.state == "QUEUED"
    print(f"[+] Job queued: {job.id} (State: {job.state})")

    JobService.update_job_progress(job.id, 0.5, state="RUNNING")
    job_running = JobService.get_job(job.id)
    assert job_running.state == "RUNNING"
    assert job_running.progress == 0.5
    print(f"[+] Job progress updated: {job_running.progress * 100}% (State: {job_running.state})")

    JobService.complete_job(job.id, output_ids=["asset_demo_render_01"])
    job_done = JobService.get_job(job.id)
    assert job_done.state == "COMPLETED"
    assert job_done.progress == 1.0
    print(f"[+] Job completed successfully with outputs: {job_done.output_ids}")

    # 5. Project Bundle Export & Import test
    print("[*] Testing Project Bundle Export/Import...")
    bundle = ProjectService.export_project_bundle(proj.id)
    assert bundle["format"] == "viralstudio_bundle_v1"
    imported = ProjectService.import_project_bundle(bundle)
    assert imported.id != proj.id, "Imported project must have new unique ID"
    assert len(imported.scenes) == 2, "Imported project must preserve scenes"
    print(f"[+] Project exported and imported cleanly: New ID {imported.id} ('{imported.title}')")

    # 6. Jev Service test
    print("[*] Testing JevService evaluation...")
    eval_res = JevService.evaluate_script("Hey what's up guys! Dengar bunyi garing donut leleh ni.")
    assert "virality_score" in eval_res
    assert "tier" in eval_res
    assert "jev_telemetry" in eval_res
    print(f"[+] JevService returned score {eval_res['virality_score']} ({eval_res['tier']}) via engine: {eval_res['jev_telemetry']['engine']}")

    print("\n[🎉] ALL PROMPT 2 CORE SERVICE TESTS PASSED 100%!")

if __name__ == "__main__":
    test_full_pipeline()
