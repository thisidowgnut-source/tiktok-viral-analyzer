# Suara dan saluran video UGC

## Aliran sebenar

1. Pengguna memilih suara dan kadar, kemudian menghantar skrip melalui `/api/tts` atau `/api/render-video`.
2. `edge-tts` menghantar teks ke perkhidmatan suara Microsoft melalui internet dan menyimpan MP3 dalam `static/exports`. Nama cache audio bergantung pada teks, suara dan kadar.
3. FFprobe membaca durasi MP3. Untuk render, kod memecahkan skrip kepada ketulan **enam perkataan** dan membahagikan jumlah durasi audio sama rata untuk menghasilkan SRT.
4. FFmpeg mengulang video latar, memotong dan menskalakannya kepada 720×1280, membakar sari kata, menambah audio AAC, lalu menulis MP4 H.264.
5. Endpoint memulangkan URL `/exports/...` untuk pratonton dan muat turun.

`asyncio.to_thread()` menjalankan proses FFmpeg di luar event loop. Ini mengelakkan satu render menyekat semua respons HTTP pada loop utama, tetapi bukan sistem antrean pekerjaan; penggunaan serentak ramai pengguna, kuota CPU, masa tamat dan pembersihan fail belum diurus.

## Status yang disahkan

- Kod semasa memasukkan nama video latar, audio dan hash skrip dalam nama MP4. Dua latar berbeza telah menghasilkan fail berlainan dalam pemeriksaan tempatan.
- Satu bingkai MP4 semasa menunjukkan teks kuning dengan garis luar hitam terbakar pada video.
- Fail yang diperiksa mempunyai video H.264 720×1280 dan audio AAC.
- Sari kata kini diagih mengikut masa secara **anggaran rata**, bukan penjajaran perkataan atau fonem. Panjang setiap ketulan ialah enam perkataan; tempohnya berubah dengan durasi keseluruhan.

## Had penggunaan

- `edge-tts` bukan TTS offline. Sambungan internet diperlukan untuk audio baharu, dan kandungan skrip dihantar kepada perkhidmatan luaran.
- Video eksport menggunakan klip latar yang sudah wujud. Ia tidak menjana rakaman baharu, melakukan suntingan pelbagai syot, menambah kesan bunyi seperti yang dicadangkan dalam skrip, atau menerbitkan ke TikTok.
- `bg_video` tidak disahkan terhadap senarai nama yang dibenarkan dan kod boleh memilih video pertama secara senyap jika nama yang diminta tiada. Tambah validasi sebelum penggunaan luas.
- Fail MP3, SRT dan MP4 terkumpul dalam `static/exports`; belum ada dasar tamat tempoh atau pembersihan.
- Tiada had panjang skrip dan tiada ujian beban render berbilang pengguna.

## Semakan fail hasil

```powershell
ffprobe -v error -show_entries stream=codec_name,width,height:format=duration -of json 'static\exports\NAMA_FAIL.mp4'
```

Semak bingkai pada beberapa masa video, dengar audio, bandingkan latar yang dipilih, dan pastikan durasi serta sari kata sesuai. HTTP 200 sahaja tidak membuktikan video tepat.
