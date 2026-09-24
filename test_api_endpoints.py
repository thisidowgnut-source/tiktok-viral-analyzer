"""
Test script for live REST API endpoints of ViralStudio.
Tests:
1. GET /api/videos?hook=CRAVING_SENSORY (P0 hook filter fix)
2. GET /api/projects (SQLite persistence)
3. POST /api/projects (Project creation)
4. GET /sw.js (PWA service worker root scope)
5. POST /api/score (Jev System One answers extraction)
"""

import sys
import json
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "http://127.0.0.1:8765"

def test_live_api():
    print("[*] Testing live endpoints on", BASE_URL)

    # 1. GET /api/videos?hook=CRAVING_SENSORY
    url_v = f"{BASE_URL}/api/videos?hook=CRAVING_SENSORY&limit=5"
    req_v = urllib.request.urlopen(url_v)
    videos = json.loads(req_v.read().decode("utf-8"))
    assert len(videos) > 0, "GET /api/videos?hook=CRAVING_SENSORY must return matching videos"
    print(f"[+] GET /api/videos?hook=CRAVING_SENSORY returned {len(videos)} videos (First: '{videos[0]['title']}', Hook: '{videos[0]['hook_type']}')")

    # 2. GET /api/projects
    url_p = f"{BASE_URL}/api/projects"
    req_p = urllib.request.urlopen(url_p)
    projects = json.loads(req_p.read().decode("utf-8"))
    print(f"[+] GET /api/projects returned {len(projects)} persistent projects from SQLite")

    # 3. POST /api/projects
    new_proj_payload = json.dumps({
        "title": "Kempen Viral Donut Coklat Lava",
        "language": "ms",
        "brief": {"niche": "Food & Beverage", "product": "Nutella Hazelnut"}
    }).encode("utf-8")
    req_create = urllib.request.Request(
        f"{BASE_URL}/api/projects",
        data=new_proj_payload,
        headers={"Content-Type": "application/json"}
    )
    res_create = urllib.request.urlopen(req_create)
    created_proj = json.loads(res_create.read().decode("utf-8"))
    assert created_proj["id"] is not None
    assert created_proj["title"] == "Kempen Viral Donut Coklat Lava"
    print(f"[+] POST /api/projects created: {created_proj['id']} - '{created_proj['title']}' (Status: {created_proj['status']}, Version: {created_proj['version']})")

    # 4. GET /sw.js (Header check)
    req_sw = urllib.request.urlopen(f"{BASE_URL}/sw.js")
    sw_header = req_sw.headers.get("Service-Worker-Allowed")
    assert req_sw.status == 200
    assert sw_header == "/", f"Expected Service-Worker-Allowed: /, got {sw_header}"
    print(f"[+] GET /sw.js returned HTTP 200 with Service-Worker-Allowed: '{sw_header}' (PWA root scope active)")

    # 5. POST /api/score
    score_payload = json.dumps({
        "script": "Dengar bunyi garing donut salted egg ini. Cuba sekarang!"
    }).encode("utf-8")
    req_score = urllib.request.Request(
        f"{BASE_URL}/api/score",
        data=score_payload,
        headers={"Content-Type": "application/json"}
    )
    res_score = urllib.request.urlopen(req_score)
    score_data = json.loads(res_score.read().decode("utf-8"))
    assert "virality_score" in score_data
    assert "jev_telemetry" in score_data
    assert "AttributeError" not in score_data["jev_telemetry"].get("engine", "")
    print(f"[+] POST /api/score returned virality_score: {score_data['virality_score']} ({score_data['tier']}) - Engine: {score_data['jev_telemetry']['engine']}")

    print("\n[🎉] ALL LIVE API ENDPOINT TESTS PASSED 100%!")

if __name__ == "__main__":
    test_live_api()
