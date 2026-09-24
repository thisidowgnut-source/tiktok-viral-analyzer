# Pembangunan, ujian dan jurang terbuka

## Persekitaran

Jalankan dari direktori projek pada mesin Windows yang mempunyai Python dan FFmpeg/FFprobe. `app.py` menggunakan laluan mutlak untuk projek ini dan aset `C:\Users\User\projects\Doh-Nut\public`. `typesafe-system-one` ialah projek saudara pilihan untuk scorer. UI menggunakan CDN; TTS baharu memerlukan internet.

```powershell
cd C:\Users\User\projects\tiktok-viral-analyzer
python -m pip install fastapi uvicorn pydantic edge-tts playwright pytest
python -m playwright install chromium
python app.py
```

Perintah di atas memasang pakej asas yang diimport oleh aplikasi dan skrip ujian; ia belum dikunci oleh fail dependency projek. Buka `http://127.0.0.1:8765`. Jangan jadikan pelayan ini deployment awam tanpa kerja keselamatan tambahan.

## Semakan pantas yang boleh diulang

```powershell
python -m py_compile app.py virality_scorer.py viral_script_generator.py a2a_engine.py
python -m pytest -q test_strict_validation.py
Invoke-RestMethod -Uri 'http://127.0.0.1:8765/api/stats'
Invoke-RestMethod -Uri 'http://127.0.0.1:8765/api/videos?hook=CRAVING_SENSORY'
Invoke-RestMethod -Uri 'http://127.0.0.1:8765/api/score' -Method Post -ContentType 'application/json' -Body '{"script":"Dengar bunyi garing donut ini."}'
```

Semak `jev_telemetry.engine` dalam respons skor. Semasa audit, respons menyatakan `local_fallback (AttributeError)` walaupun HTTP 200. Penapis hook mengembalikan senarai kosong walaupun fail data mengandungi label itu. Kedua-duanya ialah ujian regresi yang perlu bertukar kepada hasil betul selepas pembaikan.

`test_strict_validation.py` menulis semula `validated_output_sample.json` apabila dijalankan. Skrip `test_dohnut_tab.py`, `test_enhanced_ui.py`, `test_new_features.py`, `test_teleprompter.py`, `test_webapp_tabs.py` dan `verify_sota_ui.py` menjalankan Playwright terhadap server yang sudah hidup dan mungkin menulis tangkapan skrin ke direktori luar projek. Semak sasaran sebelum menjalankannya. Kebanyakan skrip itu ialah pemeriksaan visual/ad hoc, bukan suite yang mengesahkan semua tuntutan produk. Tiada ujian automatik khusus bagi ketepatan data 363, kalibrasi skor, cache eksport dan penjajaran sari kata.

## Semakan video yang bermakna

1. Jana dua video dengan audio dan skrip sama tetapi latar berbeza; URL serta kandungan MP4 mesti berbeza.
2. Jana video dengan beberapa ayat; lihat bingkai awal, tengah dan akhir untuk memastikan sari kata muncul pada masa munasabah.
3. Gunakan FFprobe untuk sahkan 720×1280, H.264, AAC dan durasi yang sepadan dengan audio.
4. Semasa FFmpeg berjalan, uji `/api/stats`; respons tidak patut menunggu render siap.
5. Uji teks panjang, suara/kadar tidak sah, video latar tidak wujud dan storan hampir penuh. Catat ralat yang dipaparkan kepada pengguna.

## Jurang utama yang perlu ditutup

| Keutamaan | Isu | Kriteria siap |
| --- | --- | --- |
| P0 | 296/363 rekod tiada metrik tontonan; tiada transkrip untuk analisis hook. | Papar data hilang secara jelas, audit sumber, dan gunakan label rujukan bagi dakwaan analitik. |
| P0 | Scorer membaca `resp.results` sedangkan klien semasa menyediakan `answers`. | Respons menamakan enjin sebenar dan menggunakan nilai model yang diuji; fallback tidak dilabel sebagai Jev Cloud. |
| P1 | API/UI menjangka `hook_analysis.hook_type`, dataset menyimpan `hook_type` rata. | Penapis, carta dan butiran video menggunakan satu skema serta ujian lulus. |
| P1 | Tier tontonan, retensi kempen dan skor A2A tinggi ialah nilai tetap/andaian. | Papar sebagai contoh atau gantikan dengan ukuran yang diuji terhadap hasil sebenar. |
| P1 | Eksport tidak ada had input, kuota, antrean dan pembersihan. | Had dan dasar storan dinyatakan serta diuji di bawah beban. |
| P2 | Laluan Windows mutlak dan tiada dependency lock. | Pemasangan boleh diulang pada mesin lain dengan konfigurasi. |
| P2 | Service worker berdaftar di bawah `/static/`. | Ujian offline dan pemasangan PWA pada skop halaman utama lulus. |

## Cara melapor hasil

Nyatakan tarikh, versi/fail yang diuji, input, output sebenar, status enjin Jev, dan had ujian. “0 ralat konsol” atau satu tangkapan skrin ialah bukti untuk sesi itu sahaja, bukan pengesahan seluruh sistem.
