# Inventori Google Apps & Analisis Aliran Kerja Opal — 24 September 2026

## 1. Status Akses Persekitaran & Pengesahan Profil

- **Chrome Profil Operasi**: `dohnut` (`thisisdohnut@gmail.com`).
- **Google Flow**: PRO Tier disahkan aktif (1,020 Flow credits direkodkan pada semakan awal; baki tertakluk pada penggunaan). Sesuai untuk penjanaan b-roll video generatif.
- **Google Opal**: Galeri 22 aplikasi aktif boleh diakses melalui pemilih akaun.
- **Google AI Studio / Gemini API**: SDK `google-genai` v1.65.0 dipasang secara rasmi dalam persekitaran Python. Adapter pelayan `services/google_adapter.py` dibina dengan fallback deterministik untuk mod luar talian tanpa API key.
- **NotebookLM**: Sumber rujukan fakta kempen (DOH-NUT ground truth: GangNiaga Sdn. Bhd., 31 perisa, brioche sourdough 48 jam).
- **Google Stitch**: Reka bentuk asas skrin Studio & Dashboard (5 paparan: Utama, Projek, Studio, Aset, Analitik).

---

## 2. Pemetaan Komprehensif 22 Aplikasi Opal (Input, Output, Model & Peranan)

Berdasarkan pemeriksaan galeri Opal, 6 aplikasi teras diutamakan untuk saluran video pendek, manakala 16 aplikasi lain dikategorikan dengan status dan justifikasi teknikal yang jelas:

### A. 6 Aplikasi Teras Diutamakan (High-Priority Workflow)

| Aplikasi Opal | Input Sebenar / Dijangka | Output Berstruktur | Model / Enjin | Peranan dalam ViralStudio |
|---|---|---|---|---|
| **1. Video Marketer** | Nama produk, USP, sasaran audiens, durasi (15-30s) | Rangka babak video (narration, visual cue, on-screen text) | Gemini 1.5/2.5 Pro | Enjin cadangan babak dan pengarahan visual automatik dalam Studio Langkah 1 & 2. |
| **2. Video Hooks Brainstormer** | Topik produk, sudut emosi (ASMR / FOMO / Relatable) | 5 variasi ayat hook pembuka 0-3 saat berimpak tinggi | Gemini Flash / Jev System One | Mengisi pilihan Hook dalam penjana skrip dan penilaian virality scorer. |
| **3. Product Marketing** | Ciri-ciri produk DOH-NUT, promosi aktif (Free delivery > RM25) | Teks positioning, sudut jualan unik, cadangan CTA Beg Kuning | Gemini Flash | Menjamin mesej penukaran jualan (conversion copy) kekal selaras dengan panduan jenama. |
| **4. Marketing Maven** | Objektif kempen TikTok Shop, bajet, platform | Cadangan jadual posting, taktik interaksi komen, audio trend | Gemini Pro | Memberikan panduan pengedaran selepas video selesai dieksport. |
| **5. Social Media Post** | Skrip video terpilih, hashtag sasaran (#dohnut #foodiekl) | Kapsyen TikTok/Reels padat dengan emoji & soalan interaksi | Gemini Flash | Dihasilkan bersama pakej eksport MP4 untuk memudahkan pencipta copy-paste. |
| **6. Sticker Generator** | Konsep pelekat ("LAVA MELELEH", "HOT & FRESH", "BEG KUNING") | Prompt visual pelekat / aset grafik PNG telus | Imagen 3 / SVG Canvas | Sumber aset visual overlay untuk dibakar ke atas babak video melalui FFmpeg. |

---

### B. 16 Aplikasi Galeri Opal Tambahan (Secondary / Contextual Inventory)

| Aplikasi Opal | Kategori & Potensi Kegunaan | Status Ujian | Catatan / Sebab Tidak Relevan untuk Aliran Teras Video |
|---|---|---|---|
| **7. Co-Thinker** | Penilaian strategi & keputusan perniagaan | Diperiksa | Berguna untuk brainstorm hala tuju syarikat, tetapi terlalu umum untuk penjanaan skrip video pantas. |
| **8. Product Research** | Kajian pasaran pencuci mulut / donat | Diperiksa | Rujukan latar belakang; data asas produk DOH-NUT sudah disahkan dalam NotebookLM/Brand Kit. |
| **9. Recipe Genie** | Variasi resipi donat & ramuan | Diperiksa | DOH-NUT menggunakan 31 perisa berdaftar kilang GangNiaga; dilarang mereka cipta resipi baru tanpa kelulusan jenama. |
| **10. Claymation Explainer** | Konsep animasi tanah liat | Diperiksa | Menarik untuk gaya eksperimental, namun aliran utama mengutamakan visual realistik makanan (craving sensory). |
| **11. Topic Explainer** | Penjelasan bersumber topik umum | Diperiksa | Kurang sesuai untuk video jualan pendek 15 saat; lebih sesuai untuk video panjang YouTube. |
| **12. Visual Storyteller** | Penceritaan visual interaktif | Diperiksa | Potensi untuk konsep video bersiri (episod), tetapi di luar skop MVP Studio 4-Langkah. |
| **13. Room Styler** | Reka bentuk ruang / hiasan bilik | Diperiksa | Tidak relevan secara langsung untuk penghasilan video produk makanan F&B. |
| **14. Interior Designer** | Susun atur set kedai fizikal | Diperiksa | Boleh dirujuk jika membuka cawangan kiosk fizikal baru, bukan untuk skrip TikTok harian. |
| **15. Fashion Stylist** | Pakaian bakat / host video | Diperiksa | Host video DOH-NUT memakai apron berjenama atau baju kasual streetwear; cadangan gaya automatik belum diperlukan. |
| **16. Learning with YouTube** | Analisis video tutorial YouTube | Diperiksa | ViralStudio sudah mempunyai enjin analitik 363 video Khairul Aming khusus untuk pasaran tempatan. |
| **17. Personal Podcaster** | Penjanaan audio podcast | Diperiksa | Format audio panjang; video TikTok memerlukan audio pendek 15-30 saat dengan suara Azure Yasmin/Osman. |
| **18. Create a Playlist** | Mood muzik latar belakang | Diperiksa | Status hak cipta muzik luaran di TikTok berisiko; video kini dijana dengan suara tulen & sound effects tempatan. |
| **19. Game Concept Builder** | Gamifikasi kempen | Diperiksa | Di luar skop penghasilan video pendek standard. |
| **20. Google Calendar Link** | Penjadualan pelancaran | Diperiksa | Pengguna boleh menjadualkan secara terus di TikTok Creator Center atau kalendar peribadi. |
| **21. Business Profiler** | Profil reputasi korporat | Diperiksa | Relevan untuk audit jenama tahunan, bukan untuk rendering video berulang. |
| **22. Book Recs** | Cadangan buku perniagaan/pemasaran | Diperiksa | Nilai tambah peribadi, tiada kaitan fungsian dengan compositor video FFmpeg. |

---

## 3. Seni Bina Adapter Pelayan (Google AI Studio & Jev System One)

Untuk mengelakkan kebocoran rahsia dan kebergantungan tegar pada perkhidmatan awan:
1. **Pemisahan Kredensial**: Kunci API disimpan dalam pembolehubah persekitaran (`GEMINI_API_KEY`, `GOOGLE_API_KEY`). Tiada kunci dibenamkan dalam frontend.
2. **Offline-First Fallback Path**: Jika tiada kunci API atau berlaku ralat kuota (HTTP 429), adapter `GoogleAIStudioAdapter` bertukar secara automatik kepada templat DOH-NUT tempatan yang disahkan.
3. **Pematuhan Jev Prompt G8**: Menggunakan 4 kaedah berstruktur:
   - `JevService.classify_route`: Mengklasifikasikan aliran kerja (`upload_existing`, `generate_image`, dsb.).
   - `JevService.evaluate_brief_status`: Menyemak kesempurnaan brief (`sufficient`, `missing_product_facts`, `missing_objective`).
   - `JevService.evaluate_script_quality`: Rubrik 4-paksi (Kejelasan, Ketepatan Fakta, Kesesuaian CTA, Kesesuaian Durasi). Sifar tekaan spekulatif tontonan.
   - `JevService.evaluate_revision_action`: Arahan semakan berstruktur (`accept_for_preview`, `revise_once`, `request_missing_input`).
