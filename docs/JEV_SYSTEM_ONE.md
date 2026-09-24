# Jev System One dan skor ViralStudio

## Peranan Jev yang sesuai

TypeSafe Jev System One ialah enjin keputusan bertipe. Dalam projek ini, klien Python luaran berada di `C:\Users\User\projects\typesafe-system-one`. Ia boleh mengelaskan pilihan dan skor yang ditakrifkan, tetapi ia tidak menulis skrip, mengesahkan prestasi TikTok, atau menggantikan dataset berlabel. Perlu bezakan respons `cloud` daripada enjin `local` heuristik.

## Laluan semasa dalam kod

| Aliran | Perilaku yang disemak |
| --- | --- |
| Analisis 363 rekod | `analyze_all_363_videos.py` menggunakan `mode="local"`, berdasarkan tajuk, durasi dan tontonan; tiada transkrip. |
| Skor skrip langsung | `virality_scorer.py` membuat `TypeSafeClient()` dalam mod auto, tetapi membaca `resp.results`; klien semasa menyediakan `resp.answers`. Respons endpoint yang diuji melaporkan `local_fallback (AttributeError)`. |
| Skor akhir | Bermula daripada 7.0 jika bacaan Jev gagal, kemudian tambah/tolak nilai tetap untuk kata kunci deria, rasa ingin tahu, panjang hook dan pacing. |
| Tier/retensi/tontonan | Dipilih daripada ambang tetap pada skor akhir; belum dikalibrasi menggunakan hasil sebenar. |

Contoh input “Dengar bunyi garing donut ini. Cuba sekarang!” mengembalikan skor 8.2, tier “200k–1M views” dan retensi “55%–75%”, sambil telemetri menyatakan `local_fallback (AttributeError)`. Angka tontonan/retensi itu ialah **label senario dalam kod**, bukan ramalan yang diuji secara empirikal. Keyakinan lalai `0.75`/`0.80` juga bukan keyakinan Jev Cloud.

## Perbaikan integrasi yang diperlukan

1. Ubah pembaca respons kepada API semasa (`resp.answers[...].value`), dan rekod `resp.engine` bagi setiap panggilan.
2. Jika panggilan cloud gagal, papar status fallback dengan jelas pada API dan UI. Jangan panggilnya skor Jev Cloud.
3. Pisahkan skor model daripada pelarasan peraturan supaya pembaca dapat melihat sumbangan masing-masing.
4. Uji terhadap set skrip dan hasil sebenar yang dilabel; ukur ralat dan kalibrasi sebelum menamakan julat tontonan atau retensi sebagai ramalan.
5. Tetapkan had masa dan had penggunaan API supaya kegagalan rangkaian tidak menggantung pengalaman pengguna.

## Jev digunakan untuk semakan dokumentasi ini

Satu panggilan Jev Cloud menilai keutamaan dokumentasi dan memilih bahagian data/skor sebagai yang paling perlu dijelaskan. Ia mengesyorkan nada **dokumentasi prototaip dengan had yang disahkan**. Keputusan Jev itu membantu susunan kerja; fakta dalam dokumen ini disemak pada kod dan fail data tempatan.
