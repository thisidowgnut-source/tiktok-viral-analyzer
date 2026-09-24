# ViralStudio KA-363

ViralStudio ialah prototaip studio kandungan video pendek untuk jenama DOH-NUT. Ia menggabungkan katalog 363 rekod video TikTok @khairulaming, dashboard, penjana skrip, skor heuristik, pratonton, suara, dan eksport MP4 menegak. Aplikasi berjalan secara tempatan pada `http://127.0.0.1:8765`.

> **Status: prototaip berfungsi.** Skor viraliti, anggaran retensi, julat tontonan, dan peratus kempen dalam UI belum disahkan sebagai ramalan prestasi sebenar. Gunakan sebagai idea kreatif, bukan jaminan hasil pemasaran.

## Apa yang ada

| Aliran | Pelaksanaan semasa |
| --- | --- |
| Intelligence Hub | Memaparkan 363 rekod dan statistik tersimpan; 296 rekod tiada angka tontonan. |
| Skrip dan skor | Skrip dijana daripada templat; skor menggunakan peraturan apabila integrasi Jev gagal. |
| Arena A2A | Simulasi peranan Zara, Tariq dan Sam dalam satu fungsi, dengan dialog berskrip. |
| DOH-NUT | Katalog, kempen dan aset daripada kod/aset tempatan. Angka retensi kempen ialah nilai tetap dalam kod. |
| Suara dan video | `edge-tts` memerlukan internet; FFmpeg menghasilkan MP4 H.264/AAC 720×1280 dengan sari kata terbakar dalam kod semasa. |
| PWA | Manifest dan service worker wujud; liputan offline untuk halaman utama belum disahkan. |

Tiada fungsi menerbitkan video terus ke TikTok, mengukur retensi sebenar selepas terbit, atau melatih model ramalan daripada dataset ini.

## Mulakan pada mesin projek asal

Prasyarat: Python, `fastapi`, `uvicorn`, `pydantic`, `edge-tts`, FFmpeg dan FFprobe pada `PATH`. Untuk skrip penuaian data dan ujian pelayar, pasang Playwright dan pelayar Chromium. Kod menggunakan laluan mutlak ke `C:\Users\User\projects\tiktok-viral-analyzer`, `Doh-Nut\public`, dan `typesafe-system-one`; ubah laluan itu sebelum menjalankan di mesin lain. Tiada fail pemasangan kebergantungan yang dikunci dalam projek ini.

```powershell
cd C:\Users\User\projects\tiktok-viral-analyzer
python -m pip install fastapi uvicorn pydantic edge-tts playwright
ffmpeg -version
ffprobe -version
python app.py
```

Buka `http://127.0.0.1:8765`. Set `PORT` jika port lalai digunakan proses lain. Server diikat pada `127.0.0.1`, jadi ia bukan deployment awam. Halaman memuatkan Tailwind, Chart.js, Three.js dan fon melalui CDN; suara juga menggunakan perkhidmatan rangkaian.

## Peta dokumentasi

- [Seni bina](docs/ARCHITECTURE.md) — komponen dan aliran data.
- [Rujukan API](docs/API_REFERENCE.md) — endpoint dan skema input.
- [Data 363 video](docs/DATASET_363_KHAIRULAMING.md) — asal, kelengkapan dan batasan data.
- [Jev dan skor](docs/JEV_SYSTEM_ONE.md) — laluan model sebenar dan skor semasa.
- [Video UGC](docs/UGC_VIDEO_PIPELINE.md) — TTS, sari kata dan FFmpeg.
- [Arena A2A](docs/A2A_MULTI_AGENT.md) — fungsi sebenar watak ejen.
- [Pembangunan dan ujian](docs/DEVELOPMENT_AND_TESTING.md) — semakan yang boleh diulang.
- [Sumbangan](CONTRIBUTING.md) — cara mengubah kod dan tuntutan produk dengan bertanggungjawab.

Dokumentasi ini berdasarkan pemeriksaan kod dan data tempatan pada **24 September 2026**. Jika kod berubah, jalankan semula semakan dalam [panduan ujian](docs/DEVELOPMENT_AND_TESTING.md) sebelum mengemas kini status.
