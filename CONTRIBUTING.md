# Panduan menyumbang

Projek ini ialah prototaip tempatan yang menggabungkan data pihak ketiga, aset jenama, perkhidmatan TTS awan dan enjin keputusan pilihan. Sumbangan paling bernilai ialah menjadikan sumber data, keputusan dan output video boleh diuji serta diterangkan dengan tepat.

## Sebelum mengubah kod

1. Semak [README](README.md), [seni bina](docs/ARCHITECTURE.md) dan [isu yang diketahui](docs/DEVELOPMENT_AND_TESTING.md#jurang-utama-yang-perlu-ditutup).
2. Nyatakan modul dan perilaku yang diubah. Bezakan perubahan kod daripada perubahan teks pemasaran.
3. Jangan masukkan kunci API, token, kata laluan, profil Chrome, atau data peribadi ke dalam fail projek atau laporan.
4. Hormati hak dan syarat penggunaan data serta media pihak ketiga. Jangan anggap data TikTok atau imej/klip boleh diedarkan semula hanya kerana ia boleh dibaca secara teknikal.

## Standard perubahan

- Gunakan satu skema data yang konsisten antara JSON, API dan JavaScript UI. Contoh semasa: `hook_type` disimpan sebagai medan rata, tetapi beberapa pembaca mencari `hook_analysis.hook_type`.
- Jangan panggil keputusan heuristik setempat sebagai Jev Cloud. Rekod enjin sebenar (`cloud`, `local`, atau `fallback`) bersama keputusan.
- Jangan memaparkan angka tontonan, retensi, skor keyakinan atau “kejayaan kempen” sebagai fakta jika ia nilai contoh atau anggaran.
- Kekalkan panggilan render berat di luar event loop. Tetapkan had input, storan dan masa sebelum menawarkan penggunaan ramai pengguna.
- Sertakan semakan yang gagal sebelum pembaikan dan lulus selepas pembaikan bagi isu yang boleh diulang.

## Semakan minimum sebelum menyerahkan perubahan

```powershell
python -m py_compile app.py virality_scorer.py viral_script_generator.py a2a_engine.py
python -m pytest -q test_strict_validation.py
```

Ujian pelayar dan eksport video memerlukan server, Playwright, FFmpeg, aset DOH-NUT dan internet untuk TTS baharu. Jalankan ujian berkaitan mengikut [panduan pembangunan](docs/DEVELOPMENT_AND_TESTING.md), kemudian laporkan apa yang benar-benar diuji serta apa yang belum.

## Gaya dokumentasi

Tulis untuk pengguna yang mahu faham hasil dan hadnya. Gunakan label **disahkan**, **anggaran**, atau **simulasi** apabila perlu. Kemas kini fail dokumentasi yang terkesan dalam perubahan yang sama. Elakkan tuntutan “100% siap”, “terbukti viral”, atau “autonomi” tanpa kaedah pengesahan yang boleh diulang.
