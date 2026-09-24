# Arena A2A Zara, Tariq dan Sam

Arena ini membantu pengguna melihat cara idea iklan DOH-NUT boleh diperhalus melalui tiga sudut pandang: strategi hook, kritikan skor, dan arahan produksi. Ia ialah **simulasi aliran kerja** yang dilaksanakan dalam `a2a_engine.py`, bukan sistem tiga ejen AI bebas yang bertukar mesej atau berunding secara autonomi.

## Apa yang fungsi lakukan

`run_a2a_collaboration(prompt)` mengesan beberapa kata kunci produk, menetapkan draf hook yang hampir tetap, memanggil `evaluate_script()` dua kali, memilih hook diperhalus yang tetap, menghasilkan skrip daripada templat, dan membina senarai mesej Zara–Tariq–Sam untuk UI. Ia memulangkan JSON dengan `dialogue`, `final_script`, `final_virality_score` dan konteks jenama jika prompt berkaitan DOH-NUT.

`handle_copilot_chat(message)` memulangkan respons yang ditetapkan mengikut kata kunci seperti DOH-NUT, audit atau video. Ia bukan chatbot generatif umum dan tidak menyimpan sejarah perbualan.

## Had yang perlu dipaparkan dengan jujur

- Skor akhir diletakkan pada minimum 9.2 melalui `max(9.2, refined_eval + 1.2)`. Ini menjadikannya tidak sesuai sebagai ukuran bebas kualiti idea.
- Kritikan Jev bergantung pada `evaluate_script()`. Semasa audit, scorer itu jatuh ke heuristik akibat ketidakpadanan format respons klien.
- Dialog, arahan kamera dan pilihan hook banyak yang tetap, walaupun prompt pengguna berubah.
- Tiada proses tiga ejen berasingan, memori bersama, perdebatan iteratif, atau verifikasi hasil kempen sebenar.

## Arah peningkatan

Jika produk mahu mengekalkan pengalaman simulasi, namakannya “arena idea tiga peranan” dan buang dakwaan autonomi. Jika mahu membina kolaborasi ejen sebenar, takrifkan kontrak input/output setiap ejen, log langkah keputusan, had pusingan, cara menangani kegagalan, dan ujian yang menunjukkan output benar-benar berubah mengikut prompt. Jangan paksa skor akhir ke tahap tinggi.
