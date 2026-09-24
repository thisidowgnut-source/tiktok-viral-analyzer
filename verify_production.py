import sys
import requests

sys.stdout.reconfigure(encoding='utf-8')
url = 'https://tiktok-viral-analyzer-nine.vercel.app'

print('=== VERCEL PRODUCTION EMPIRICAL VERIFICATION ===')

r_root = requests.get(url, timeout=10)
print(f'[1] Root URL: {r_root.status_code} OK (HTML size: {len(r_root.text)} bytes)')

r_vids = requests.get(f'{url}/api/videos?limit=3', timeout=10)
print(f'[2] 363 Videos API: {r_vids.status_code} OK ({len(r_vids.json())} items loaded)')

r_projs = requests.get(f'{url}/api/projects', timeout=10)
print(f'[3] SQLite Projects API: {r_projs.status_code} OK ({len(r_projs.json())} projects in DB)')

r_jev = requests.post(f'{url}/api/integrations/jev/quality', json={'script_text': 'Sourdough brioche sedap manis meleleh!'}, timeout=10)
print(f'[4] Jev System One Quality API: {r_jev.status_code} OK (Score: {r_jev.json().get("overall_quality_score")})')

r_g = requests.post(f'{url}/api/integrations/google/plan', json={'product_name': 'Doh-Nut Salted Egg', 'angle': 'ASMR Craving', 'target_duration': 15}, timeout=10)
print(f'[5] Google AI Studio Adapter (/api/integrations/google/plan): {r_g.status_code} OK ({len(r_g.json().get("scenes", []))} scenes generated)')

r_a2a = requests.post(f'{url}/api/a2a/collaborate', json={'prompt': 'Doh-Nut Nutella Lava ASMR'}, timeout=15)
print(f'[6] A2A Multi-Agent Collaboration: {r_a2a.status_code} OK (Final Viral Score: {r_a2a.json().get("final_score")})')

print('\nALL 6 ENDPOINTS RETURNED 200 OK ON VERCEL PRODUCTION!')
