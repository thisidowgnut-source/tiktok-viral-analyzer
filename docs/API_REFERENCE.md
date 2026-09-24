# Rujukan API tempatan

Alamat lalai: `http://127.0.0.1:8765`. Semua laluan di bawah dilaksanakan dalam `app.py`. Server semasa diikat pada loopback dan tidak mempunyai pengesahan pengguna. Jangan dedahkan ke rangkaian awam tanpa kawalan akses, had input dan had storan.

| Kaedah | Laluan | Input | Output utama |
| --- | --- | --- | --- |
| GET | `/` | Tiada | Halaman HTML aplikasi. |
| GET | `/api/stats` | Tiada | `MACRO_STATS` yang ditetapkan dalam kod. |
| GET | `/api/videos` | `limit`, `hook`, `q` | Senarai rekod daripada JSON 363. |
| POST | `/api/score` | `{ "script": "..." }` | Skor, hook, pacing, tier dan telemetri enjin. |
| POST | `/api/generate` | `{ "product_name": "...", "niche"?: string, "hook_style"?: string, "target_audience"?: string, "usp_points"?: string[], "include_catchphrase"?: boolean }` | Skrip templat empat fasa. |
| GET | `/api/dohnut/campaigns` | Tiada | Pengetahuan jenama dan lima kempen dalam kod. |
| POST | `/api/a2a/collaborate` | `{ "prompt": "..." }` | Dialog simulasi tiga peranan dan skrip akhir. |
| POST | `/api/a2a/chat` | `{ "message": "..." }` | Respons copilot berdasarkan kata kunci. |
| POST | `/api/tts` | `{ "text": "...", "voice"?: string, "rate"?: string }` | `audio_url`, durasi dan suara. |
| POST | `/api/render-video` | `{ "script_text": "...", "product_name"?: string, "voice"?: string, "rate"?: string, "bg_video"?: string }` | `video_url`, durasi, nama fail. |

`/static/*`, `/exports/*`, `/brand/*` dan `/videos/*` ialah fail statik jika folder sumber wujud. URL eksport memulangkan media yang dihasilkan di `static/exports`.

## Contoh permintaan

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:8765/api/stats'
Invoke-RestMethod -Uri 'http://127.0.0.1:8765/api/score' -Method Post -ContentType 'application/json' -Body '{"script":"Dengar bunyi garing donut ini."}'
Invoke-RestMethod -Uri 'http://127.0.0.1:8765/api/generate' -Method Post -ContentType 'application/json' -Body '{"product_name":"Doh-Nut Salted Egg Lava"}'
```

TTS dan render yang belum ada dalam cache akan menggunakan rangkaian Microsoft. Render video memerlukan FFmpeg, FFprobe dan fail video latar daripada `Doh-Nut/public/videos`.

## Ralat dan had semasa

- Teks kosong pada endpoint utama menghasilkan HTTP 400. Input JSON tidak sah mengikuti validasi FastAPI/Pydantic.
- Kesalahan TTS atau FFmpeg menghasilkan HTTP 500 dengan butiran ralat; jangan anggap output separa sebagai fail sah.
- `GET /api/videos?hook=CRAVING_SENSORY` kini memulangkan senarai kosong: kod API mencari `hook_analysis.hook_type`, tetapi JSON 363 menyimpan `hook_type` pada aras atas. UI juga mempunyai pembaca bercampur bagi dua bentuk ini.
- `limit` belum dihadkan pada julat selamat; teks TTS/render belum mempunyai had panjang atau kuota storan.
- Tiada endpoint untuk status pekerjaan render, pembatalan, penerbitan TikTok, atau metrik retensi sebenar.
