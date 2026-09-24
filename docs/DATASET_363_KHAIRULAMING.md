# Dataset 363 rekod @khairulaming

## Tujuan dan laluan data

`scrape_all_khairulaming_tiktok.py` cuba mengumpul video daripada profil TikTok melalui respons rangkaian `/api/post/item_list` dan pautan yang kelihatan pada halaman. Ia menyimpan `khairulaming_all_videos_catalog.json`. `analyze_all_363_videos.py` membaca katalog itu dan menghasilkan `khairulaming_all_363_analysis.json` serta CSV. `app.py` memuatkan JSON analisis untuk Hub dan endpoint `/api/videos`.

Skrip penuaian bergantung pada struktur laman dan endpoint TikTok yang boleh berubah. Tidak ada rekod dalam projek yang membuktikan dataset ini kekal lengkap atau terkini selepas masa penuaian. Jangan menjalankan semula penuaian terhadap akaun pihak ketiga tanpa menilai keperluan, hak dan syarat penggunaannya.

## Audit data tempatan pada 24 September 2026

| Pemeriksaan | Hasil |
| --- | ---: |
| Rekod dan ID video unik | 363 / 363 |
| URL video mengikut bentuk profil berkenaan | 363 |
| Rekod dengan `views` lebih daripada sifar | 67 |
| Rekod dengan `views` sifar atau tiada metrik lengkap | 296 |
| Transkrip dalam set 363 | 0 |
| Label hook `CRAVING_SENSORY` | 363 |
| Jumlah `views` yang tersimpan | 213,389,111 |

Angka 213.4 juta ialah **jumlah medan tontonan yang tersedia dalam fail**, bukan jumlah tontonan yang terbukti lengkap untuk semua 363 video. `0` dalam rekod yang datang daripada fallback DOM boleh bermaksud metrik tidak berjaya dituai; ia tidak wajar dipaparkan sebagai tontonan sebenar sifar. Contoh pertama bertajuk “City of love” tetapi dikelaskan `RESEPI_RAMADAN`, tanda bahawa label automatik perlu diaudit.

## Apa yang boleh dan tidak boleh disimpulkan

Dataset menyimpan ID, tajuk, URL, beberapa metrik, tempoh dan label yang dijana. Ia tidak menyimpan transkrip atau video sebenar bagi 363 rekod. Oleh itu, tajuk dan angka tontonan sahaja tidak cukup untuk mengesahkan perkataan hook 0–3 saat, rentak suntingan, audio, atau kadar penonton kekal menonton. Analisis empat video contoh dengan transkrip berada dalam fail berasingan dan tidak membuktikan liputan transkrip untuk 363 rekod.

`analyze_all_363_videos.py` menggunakan `TypeSafeClient(mode="local")`. Label kelompok datang daripada heuristik setempat, bukan Jev Cloud. JSON tidak menyimpan `jev_engine` per rekod. Masa pemprosesan milisaat dalam laporan kelompok tidak patut digambarkan sebagai latensi Jev Cloud.

## Semakan sebelum dataset dipakai sebagai benchmark

1. Bezakan `metric_missing` daripada angka sifar yang sah dan simpan masa kutipan bagi setiap metrik.
2. Periksa sampel rawak URL, tajuk dan angka secara manual; rekod sumber dan kaedah kutipan.
3. Dapatkan transkrip/annotasi hook yang sah jika mahu menilai pola hook atau retensi sebenar.
4. Bina set label rujukan manusia dan ukur ketepatan klasifikasi; jangan gunakan keseragaman 363/363 sebagai bukti pola kreatif.
5. Kira semula statistik dashboard daripada data yang disahkan, bukan pemalar `MACRO_STATS` dalam `app.py`.

## Contoh semakan setempat

```powershell
python -c "import json; d=json.load(open('khairulaming_all_363_analysis.json',encoding='utf-8')); print(len(d),sum(x.get('views',0)==0 for x in d),sum(x.get('views',0) for x in d))"
```

Fail JSON dan CSV dalam projek ialah snapshot. Jangan edit angka secara manual untuk menjadikan dashboard kelihatan lebih lengkap.
