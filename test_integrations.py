import urllib.request
import json

def test_endpoint(name, url, method="GET", payload=None):
    req = urllib.request.Request(url, method=method)
    if payload:
        req.add_header("Content-Type", "application/json")
        data = json.dumps(payload).encode("utf-8")
    else:
        data = None

    try:
        with urllib.request.urlopen(req, data=data, timeout=5) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            print(f"[PASS] {name} -> HTTP {resp.status}")
            return body
    except Exception as e:
        print(f"[FAIL] {name} -> {e}")
        return None

base = "http://127.0.0.1:8765"

print("--- Testing Jev & Google Integration Endpoints ---")
# 1. Jev route
test_endpoint(
    "Jev Route",
    f"{base}/api/integrations/jev/route",
    method="POST",
    payload={"brief_text": "Kempen video DOH-NUT Musang King untuk pelancaran baru TikTok"}
)

# 2. Jev brief status
test_endpoint(
    "Jev Brief Status",
    f"{base}/api/integrations/jev/brief-status",
    method="POST",
    payload={"brief_text": "Donat brioche salted egg panas meleleh untuk promosi video TikTok"}
)

# 3. Jev script quality rubric
test_endpoint(
    "Jev Script Quality Rubric",
    f"{base}/api/integrations/jev/quality",
    method="POST",
    payload={"script_text": "Sound on! Dengar bunyi krup-krap kerak doh panas DOH-NUT ni sebelum lava salted egg dia memancut! Doh brioche sourdough fermentasi 48 jam yang sangat gebu, rangup di luar dan lembut di dalam. Free delivery order atas RM25 kat beg kuning!"}
)

# 4. Jev revision action
test_endpoint(
    "Jev Revision Action",
    f"{base}/api/integrations/jev/revision",
    method="POST",
    payload={"quality_score": 8.5, "issues_count": 0}
)

# 5. Google AI Studio scene plan
test_endpoint(
    "Google Scene Plan",
    f"{base}/api/integrations/google/plan",
    method="POST",
    payload={"product_name": "Doh-Nut Nutella Lava", "angle": "ASMR Craving", "target_duration": 15}
)

# 6. Google status
test_endpoint(
    "Google Status",
    f"{base}/api/integrations/google/status",
    method="GET"
)
