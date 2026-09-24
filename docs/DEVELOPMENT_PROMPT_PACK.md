# ViralStudio — Prompt Pembangunan Lengkap

Tarikh: 24 September 2026. Kegunaan: arahan untuk ejen pelaksana seterusnya. Fail ini tidak mendakwa ciri sudah dibina. Bahasa komunikasi: Bahasa Melayu yang jelas; kod dan nama kontrak boleh dalam bahasa Inggeris.

## Cara menggunakan fail

Berikan Prompt 0 kepada ejen coding. Ejen perlu membaca keseluruhan fail, menggunakan prompt fasa mengikut urutan, dan menyimpan checkpoint. Prompt aplikasi Google ialah teks kerja untuk aplikasi masing-masing; gantikan placeholder hanya dengan fakta yang sudah diperiksa. Jangan hantar keseluruhan repositori atau rahsia kepada aplikasi luar.

Rangka liputan dan urutan fail ini dinilai melalui Jev Cloud: `covers_core_requirements` dan `audit_then_vertical_slice_then_advanced_then_release`. Semakan itu menilai ringkasan rangka, bukan mengesahkan keseluruhan teks atau hasil implementasi.

---

## Prompt 0 — Arahan induk kepada ejen pelaksana

Anda bertanggungjawab membangunkan ViralStudio daripada prototaip sedia ada menjadi studio video pendek yang boleh digunakan, diuji dan dipasang semula. Teruskan pelaksanaan dalam skop ini sehingga syarat penerimaan dipenuhi atau terdapat halangan sebenar. Jangan berhenti selepas memberi pelan sahaja.

### Lokasi dan sumber kebenaran

- Projek: `C:\Users\User\projects\tiktok-viral-analyzer`.
- Jev wrapper: `C:\Users\User\projects\typesafe-system-one`.
- Aset jenama: `C:\Users\User\projects\Doh-Nut\public`.
- Vault rujukan: `C:\Users\User\Documents\AGY-Vault` — jangan mengubahnya jika tidak diperlukan atau tanpa izin filesystem yang sesuai.
- Baca arahan repositori yang berlaku, `README.md`, `docs/IMPROVEMENT_ROADMAP.md`, `docs/GOOGLE_APPS_INVENTORY.md`, dan dokumentasi seni bina/API/pipeline/ujian sedia ada.
- Kod dan bukti runtime semasa mengatasi dakwaan dalam log lama. Semak perubahan pengguna sebelum mengedit; jangan reset atau menimpa kerja lain.

### Hasil produk

Bina aliran **Brief → Skrip → Visual Babak → Suara & Sari Kata → Pratonton → MP4** untuk pencipta kandungan dan bisnes kecil. Bahasa Melayu dan Inggeris disokong pada brief dan kandungan. DOH-NUT ialah brand pack contoh yang boleh diganti. Pengguna boleh upload bahan sendiri dan menyiapkan video tanpa wajib menggunakan semua penyedia AI.

Gunakan ekosistem Google yang pengguna pilih:

1. Flow untuk imej dan video generatif.
2. Stitch untuk reka bentuk dashboard dan studio.
3. NotebookLM untuk sumber fakta dan penyelidikan.
4. Gemini untuk idea, skrip, shot list dan prompt.
5. Opal untuk menilai seluruh galeri yang boleh diakses dan membina workflow relevan.
6. AI Studio untuk eksperimen model serta penilaian API Google yang didokumentasikan.
7. Jev sebenar untuk keputusan berstruktur dan semakan rubric.

Profil Chrome operasi diminta: dohnut, akaun `thisisdohnut@gmail.com`. Sahkan melalui UI semasa, bukan melalui nama profil sahaja. Jangan menyalin cookies atau token. Akaun ini ialah tetapan setempat; gunakan placeholder dalam keluaran GitHub awam.

Flow pernah disahkan sebagai PRO dengan 1,020 kredit ketika semakan; ini bukan baki kekal atau kebenaran membeli kredit. Opal telah memaparkan 22 entri galeri. Buka inventori untuk status sebenar. Jangan ulang setup yang sudah berjaya kecuali sambungan semasa memerlukannya.

### Kaedah kerja

- Audit dahulu, bina satu aliran lengkap yang minimum, kemudian tambah kemampuan lanjutan.
- Kekalkan FastAPI pada peringkat awal. Pecahkan monolit secara berperingkat. Gunakan SQLite untuk projek/job setempat dan migrasi skema; jangan tambah perkhidmatan teragih tanpa keperluan terbukti.
- Buat keputusan rutin sendiri berdasarkan bukti. Tanya hanya untuk maklumat wajib, akses, kelulusan berisiko atau keputusan yang tidak boleh dipulihkan.
- Gunakan alat pelayar yang disokong sesi untuk Google. Jika fungsi memerlukan API, gunakan dokumentasi rasmi dan adapter yang diuji; jangan menganggap sesi web menyediakan API.
- Jangan membeli plan/kredit, menerbitkan, berkongsi awam, atau menghantar promosi tanpa arahan khusus. Jangan menerima terma atau meluaskan akses sensitif apabila polisi alat memerlukan pengesahan.
- Elakkan tuntutan “100% siap”, “pasti viral”, “zero hallucination”, “offline” atau “ribuan pengguna” tanpa bukti yang berkenaan.
- Simpan rekod kerja selepas setiap fasa: perubahan, ujian, batasan, tugas tertunggak. Laporkan ringkas kepada pengguna.

### Keutamaan

P0: ketepatan kontrak Jev/data, projek tersimpan, aliran upload-ke-MP4, pemasangan boleh ulang.

P1: dashboard mesra pengguna, aliran Google yang disahkan, queue, kawalan kos, brand kit dan sari kata boleh edit.

P2: eksperimen variasi, format tambahan, kolaborasi bundle projek, PWA dan pengoptimuman berdasarkan ukuran.

Hasil akhir wajib: kod, migrasi, dependency terkunci, contoh konfigurasi tanpa rahsia, ujian bermakna, demo media boleh diedarkan, dokumentasi terkini, dan laporan bukti. Persediaan GitHub tidak bermaksud kebenaran publish.

---

## Prompt 1 — Audit dan pelan pelaksanaan yang boleh diuji

Baca struktur projek dan semak runtime secara terhad. Rekod keadaan awal dalam `docs/IMPLEMENTATION_STATUS.md`, termasuk versi dependency, entrypoint, route sebenar, konfigurasi path, penyedia AI, ujian dan perubahan kerja sedia ada. Kenal pasti sama ada Git telah disediakan; jangan menganggapnya wujud.

Sahkan semula isu yang pernah ditemui:

- `virality_scorer.py` membaca `results/choice/score` sedangkan wrapper menggunakan `answers/value`; fallback pernah berlaku walaupun HTTP 200.
- Penapis hook API/UI membaca medan bersarang, dataset menggunakan medan rata.
- Dataset 363 rekod: 67 views positif, 296 sifar/tiada metrik; semua label hook sama, tiada transkrip. Semak semula angka, provenance dan author ID. Nilai tidak diketahui bukan sifar prestasi.
- Skrip dan persona A2A pernah berasaskan template; skor minimum rekaan pernah digunakan. Bezakan model sebenar, template dan demo.
- Cache video pernah bertembung; pembaikan full stem/hash perlu diuji termasuk perubahan kandungan aset dengan nama sama.
- Sari kata dibakar ke MP4 tetapi masa pernah dibahagi sama rata, bukan word alignment sebenar.
- FFmpeg sudah pernah dipindahkan ke thread; semak ffprobe, timeout, queue, cancel, concurrency dan pemulihan restart.
- TTS edge-tts bergantung pada awan; jangan label inferens offline atau menyamakannya dengan kontrak API Azure rasmi tanpa bukti.
- Semak scope service worker, path mesin, input/path validation, penyimpanan fail dan asset rights.

Hasilkan backlog P0/P1/P2 dengan lokasi kod, akibat, pembaikan dan ujian penerimaan. Jalankan pemeriksaan asas yang bermakna sahaja; simpan data asal, jangan melabel ulang dataset tanpa provenance. Teruskan Prompt 2 selepas baseline direkodkan.

## Prompt 2 — Asas aplikasi dan satu aliran lengkap

Pisahkan tanggungjawab dalam modul yang jelas: konfigurasi, route, skema, servis projek/aset, adapter AI, job worker, renderer dan frontend. Sesuaikan nama folder kepada projek semasa; migrasikan satu bahagian pada satu masa. Kekalkan route lama melalui adapter atau dokumentasikan perubahan kontraknya.

Bina entiti minimum berikut dengan ID stabil dan timestamp:

- Project: tajuk, bahasa, brand kit, brief, status, versi.
- Scene: urutan, skrip, tempoh, asset ID, crop/focal point, transisi.
- Asset: jenis, sumber upload/generated/demo, path dalaman, checksum, dimensi/durasi, provenance, status semakan.
- Job: jenis, input hash, state, progress sebenar, error code, attempts, output IDs, cancellation state.
- ProviderRun: penyedia/model, versi prompt/rubric, latency, usage tersedia, anggaran kos dengan mata wang dan tarikh kadar.
- BrandKit: warna, logo/font yang dibenarkan, gaya bahasa, CTA dan fakta produk bersumber.

Tambah migrasi SQLite, autosave dengan semakan versi, validasi dan path relatif melalui konfigurasi. Setiap projek boleh dibuka semula selepas restart. Jangan membenarkan asset ID projek lain atau path arbitrari.

Siapkan aliran tanpa cloud dahulu: brief/manual script → upload video/imej → scene → suara/aset audio yang tersedia → sari kata → preview → MP4. Paparkan ketidaktersediaan TTS dengan jujur dan benarkan audio upload. Semak MP4 menggunakan metadata sebenar dan bingkai hasil.

Syarat siap: pemasangan bersih pada persekitaran sokongan boleh menyiapkan demo; restart tidak menghilangkan projek; preview merujuk manifest sama seperti eksport; tiada dependency wajib pada path peribadi.

## Prompt 3 — Dashboard melalui Stitch dan implementasi frontend

Gunakan Prompt G2 di Stitch selepas akaun disahkan. Bawa reka bentuk yang disemak ke frontend sebenar; hasil Stitch bukan bukti backend siap. Jika eksport kod tersedia, audit dan integrasikan mengikut kontrak aplikasi.

Navigasi: Utama, Projek, Aset, Analitik, Tetapan. Butang utama Cipta Video. Halaman utama memaparkan Sambung Projek, projek terkini dan queue. Statistik kajian berada dalam Analitik dengan coverage/provenance; jangan paparkan ramalan views tanpa model yang disahkan.

Studio mempunyai empat langkah utama: Brief, Skrip, Edit & Pratonton, Eksport. Visual, audio dan sari kata berada dalam langkah ketiga. Desktop: editor dan preview bersebelahan; skrin sempit: tab mudah dicapai. Gunakan label biasa dan progressive disclosure bagi tetapan lanjutan. Tiada copilot yang menutup kandungan.

Wajib: keadaan kosong/loading/error/success, autosave, pembetulan input, fokus keyboard, label form, kontras disemak, reduced motion, modal yang memulihkan fokus, teks status bukan warna sahaja, CTA disabled dengan penjelasan apabila input belum lengkap. Preview mesti mengikut tetapan projek sebenar.

Brand DOH-NUT mesti bersumber daripada aset projek. Jangan memasukkan catchphrase pencipta lain secara lalai. Kekalkan 3D hanya sebagai pilihan showcase, lazy-load dan sediakan fallback.

Syarat siap: uji aliran dengan keyboard dan viewport lebar/sempit; capture screenshot hasil implementasi, semak ia sepadan dengan reka bentuk; tiada scroll mendatar yang tidak disengajakan; pengguna boleh pulih daripada input salah dan render gagal.

## Prompt 4 — Jev dan pipeline Google sebenar

Baca kontrak wrapper Jev yang dipasang. Gunakan cloud apabila tersedia, dan rekod `engine` sebenar. Fallback heuristik mesti dilabel sebagai fallback. Validate skema dan pilihan sebelum memanggil; jangan menggunakan confidence sebagai kebarangkalian viral.

Jev bertugas memilih workflow, mengesan medan brief yang hilang, menilai rubric skrip dan menentukan sama ada pembaikan diperlukan. Validasi deterministik dahulu, kemudian Jev, kemudian model generatif hanya untuk penulisan/pembaikan yang perlu. Hadkan rounds dan bajet. Cache dengan input, penyedia, model, rubric/prompt version dan checksum aset. Jangan memberi Jev tugas penjanaan piksel atau semakan visual yang inputnya tidak disokong.

Sahkan akses aplikasi Google melalui UI. Inventorikan setiap entri galeri Opal yang kelihatan; buka editor/view yang sesuai dan rekod model/tools, input, output, URL dan status. Gunakan semua aplikasi yang relevan mengikut peranan; catat dengan jelas aplikasi tidak relevan/terhalang, bukannya menandakan semua berjaya. Jangan jalankan batch yang menghabiskan quota hanya untuk melengkapkan checklist.

Laluan operasi pertama: NotebookLM sumber → Gemini skrip/shot list → Jev keputusan berstruktur → Opal workflow → Flow media → import ke ViralStudio → preview/render. Stitch digunakan untuk UI. AI Studio digunakan untuk eksperimen dan adapter API rasmi jika boleh diakses.

Bezakan status integrasi: browser workflow, import/export, documented API, unavailable. Langganan web tidak membuktikan akses/billing API. Jangan mengandaikan API bagi Opal/Stitch/NotebookLM atau menggunakan endpoint dalaman yang tidak disokong sebagai kontrak produksi.

Kontrak dalaman yang dicadangkan: upload assets; create image/video job; get job; request cancellation; choose scene asset; render project. Sesuaikan route sedia ada, dokumentasikan request/response/error dan idempotency. Job pelayar tidak boleh dilabel backend automatik apabila masih menunggu tindakan luar.

Uji satu kempen DOH-NUT bersumber: skrip BM, imej hero, klip video sebenar melalui Flow, import aset, sari kata, preview dan MP4. Gunakan model/durasi/resolusi yang benar-benar tersedia. Jangan membeli plan/top-up. Jika kuota atau akses menghalang, teruskan bahagian bebas dan tandakan job blocked dengan sebab tepat.

## Prompt 5 — Render, sari kata, kos dan ketahanan

Bina queue berstatus persisten dengan concurrency boleh konfigurasi. Jangan menyekat event loop dengan ffmpeg/ffprobe. Hadkan sumber CPU/RAM secara munasabah berdasarkan ukuran mesin. Gunakan proses terkawal dengan timeout, stdout/stderr terhad dan penghentian proses anak apabila dibatalkan.

Input cache merangkumi audio, suara/rate, teks/timing, kandungan video/imej, font, crop, output preset, model dan renderer version. Fail output ditulis atomik; cached success hanya apabila fail lengkap disahkan. Deduplicate permintaan sama; retry idempotent dan terhad. Selepas restart, job separuh siap ditanda interrupted/recoverable, bukan sukses palsu.

Sari kata: gunakan timestamp penyedia/ASR apabila tersedia dan disahkan. Benarkan edit teks/timing, import/export SRT atau VTT, serta label approximate untuk pembahagian masa anggaran. Letakkan teks dalam safe area, uji keterbacaan dan pembalutan; jangan menjanjikan word-perfect sync tanpa ukuran.

Mula dengan preset 9:16 H.264/AAC yang disahkan. Tambah 1:1/16:9 hanya selepas crop/preview/export diuji. Paparkan metadata output sebenar, bukan angka hardcoded. Pan/zoom pada imej hendaklah dilabel komposisi, bukan generative video.

Kos: had bilangan job/variasi, reservasi bajet sebelum dispatch, usage sebenar jika tersedia, kos unknown jika tidak dapat dihitung. Elakkan retry berbayar selepas timeout yang hasilnya tidak pasti. Cancel awan mungkin tidak menghentikan caj; paparkan batasan. Jangan menyimpan credentials dalam frontend, log, repo atau bundle.

Syarat siap: dua render serentak tidak merosakkan fail; API masih responsif dengan beban terukur; cancel dan restart tidak meninggalkan worker liar; path traversal/input rosak ditolak; cleanup tidak memadam aset projek aktif.

## Prompt 6 — Bukti ujian dan dokumentasi

Tulis ujian bagi risiko sebenar: kontrak Jev, fallback, schema dataset/filter, autosave/version conflict, isolasi aset, cache collisions, queue/cancel/restart, provider timeout/429, deduplication/budget, dan preview/export. Mock untuk ujian deterministik; sekurang-kurangnya satu ujian langsung bagi setiap integrasi yang didakwa berfungsi apabila akses tersedia.

Jalankan satu E2E upload-ke-export dan satu E2E Google-ke-export jika akses membenarkan. HTTP 200 dan sifar console error sahaja tidak mencukupi. Sahkan fail wujud, boleh dibuka, codec/dimensi/audio/durasi betul dan sari kata kelihatan pada beberapa bingkai. Simpan command, masa, versi, keputusan dan batasan tanpa rahsia.

Kemas kini README, CONTRIBUTING, ARCHITECTURE, API_REFERENCE, JEV_SYSTEM_ONE, UGC_VIDEO_PIPELINE, A2A_MULTI_AGENT, DATASET_363_KHAIRULAMING, DEVELOPMENT_AND_TESTING, GOOGLE_APPS_INVENTORY dan IMPLEMENTATION_STATUS. Tambah panduan konfigurasi/troubleshooting serta rekod keputusan seni bina jika perlu. Asingkan current/experimental/planned/blocked.

Syarat siap: dokumentasi route sepadan dengan aplikasi, link dalaman sah, quickstart diuji, hasil ujian boleh diulang. Jangan menulis rekod vault atau task board “Done” sebelum gate yang berkenaan lulus.

## Prompt 7 — Persediaan keluaran GitHub

Sediakan README yang menjelaskan siapa pengguna, masalah yang diselesaikan, demo pendek, contoh MP4, quickstart dan batasan. Mod demo tanpa key mesti menggunakan output prajana yang dilabel; jangan menyamar sebagai penjanaan langsung.

Sediakan dependency lock, `.env.example`, `.gitignore`, pemeriksaan FFmpeg, CI bagi OS yang benar-benar disokong, issue/PR templates, CONTRIBUTING, SECURITY, CODE_OF_CONDUCT, changelog dan release checklist. LICENSE memerlukan pilihan pemilik serta hak kod/aset yang jelas; jangan mereka pemilikan. Asingkan media berlesen, akaun peribadi dan dataset yang belum mendapat hak pengedaran daripada repo awam.

Jangan janjikan paling viral. Ukur pemasangan berjaya, eksport pertama, masa-ke-hasil, kegagalan dan contributor sebenar. Telemetry tambahan mestilah opt-in. Sediakan draf release serta bahan demo; tunggu arahan khusus sebelum publish atau promosi.

---

## Prompt G1 — NotebookLM: brief bersumber

Anda menyusun brief kempen DOH-NUT daripada sumber yang saya masukkan. Bina jadual fakta: claim, sumber, petikan/lokasi sokongan, tarikh dan status pengesahan. Bezakan fakta produk, hipotesis pemasaran dan angka yang belum disahkan. Jangan menganggap laporan lama “100% siap” sebagai bukti.

Hasilkan: ringkasan jenama; produk/perisa yang benar-benar wujud; persona sasaran sebagai hipotesis; tiga sudut kempen; senarai perkara yang tidak boleh didakwa; brief satu halaman untuk penulis skrip. Jika harga, bahan atau kelebihan tidak bersumber, tulis belum disahkan. Kekalkan rujukan bagi semua claim penting.

## Prompt G2 — Stitch: dashboard dan studio

Design a responsive web app called ViralStudio: a Malay-first short-video studio for small businesses, with English support and an optional DOH-NUT brand kit. The primary workflow is Brief → Script → Edit & Preview → Export. Design real task-focused screens, not a marketing landing page.

Create Home, Projects, Asset Library, Script/Scene Studio, Render Queue and Settings. Home prioritizes Create Video and Resume Project. The studio has editable scenes, source-labelled assets, voice/caption controls and a synchronized vertical preview. On narrow screens use Edit/Preview tabs. Put advanced provider controls behind disclosure. Include empty, loading, error, success, offline/provider-unavailable and quota-exhausted states.

Use one restrained accent, clear type hierarchy, consistent spacing, readable controls and keyboard focus. Do not place a floating chat over the workspace. Include save status, actionable errors and truthful progress. Show research statistics only in Analytics with provenance and missing-data labels. No guaranteed virality metrics. Use supplied brand assets only; mark missing assets as placeholders. Provide design tokens and exportable layout/code if supported. Explain how desktop and narrow-screen layouts change.

## Prompt G3 — Gemini: skrip dan shot list

Gunakan brief bersumber berikut: [BRIEF_DISAHKAN]. Brand kit: [BRAND_KIT]. Bahasa: [BM_ATAU_EN]. Tujuan: [OBJEKTIF]. Durasi sasaran: [DURASI]. Aset rujukan tersedia: [SENARAI_ASET].

Hasilkan tiga pendekatan skrip yang berbeza, dengan hook, isi dan CTA. Jangan meniru catchphrase individu tertentu secara lalai, mereka fakta/harga atau menjanjikan views. Bagi setiap pendekatan, tulis sebab pemilihan, anggaran durasi yang dilabel anggaran dan perkara untuk disemak.

Untuk pilihan utama, hasilkan shot list berstruktur: scene_id, narration, on_screen_text, target_duration, visual_description, reference_asset, camera_motion dan sound_direction. Sediakan prompt imej serta prompt video berasingan untuk setiap babak. Kekalkan rupa produk berdasarkan rujukan; letakkan harga/logo/CTA sebagai overlay boleh edit jika sesuai. Jangan mendakwa aset sudah dijana.

## Prompt G4 — Flow: imej hero

Create a high-quality product campaign still for DOH-NUT using the attached verified product reference. Product: [PRODUCT_FROM_BRIEF]. Preserve its recognizable shape, toppings, filling and packaging; do not add unsupported ingredients. Visual direction: [SELECTED_DIRECTION]. Lighting: appetizing studio light, realistic food texture, controlled reflections. Composition: vertical social-video framing with clean negative space for editable captions and CTA. No invented logo, text, price, watermark removal request or fake customer endorsement. Output one variation initially using the available image settings. Keep the product clearly readable at small screen size.

Gunakan prompt ini hanya selepas rujukan dipilih. Semak hasil berbanding asal; simpan model, prompt dan tetapan UI sebenar. Jangan menyatakan produk tepat tanpa semakan.

## Prompt G5 — Flow: klip video

Create a vertical product video from the approved reference image and this shot description: [SHOT_DESCRIPTION]. Keep the product and packaging consistent with the reference. Camera movement: [CAMERA_MOVE]. Action: [ACTION_SUPPORTED_BY_REFERENCE]. Lighting and setting: [DIRECTION]. Avoid morphing, duplicated objects, distorted food, unreadable generated text and unnecessary scene cuts. Leave room for captions and CTA added later in the editor. Audio direction, only if supported: [AUDIO_DIRECTION]. Use a duration and resolution available in this account; do not claim unavailable settings.

Jana satu klip percubaan dahulu. Semak motion, konsistensi, audio dan kesesuaian crop sebelum variasi tambahan. Jangan upscale atau ulang berbayar tanpa keperluan nyata. Simpan hasil dengan provenance sebelum import ke studio.

## Prompt G6 — Opal: workflow kempen

Build or remix a workflow named “DOH-NUT Campaign Studio” using only tools and models actually available in this Opal editor. Inputs: verified brand brief, product reference, audience, language, objective and target duration. Steps: validate required facts → propose script variants → choose a script → generate scene prompts → generate supported media or produce explicit handoff instructions → output a scene-by-scene campaign package.

Keep source facts separate from creative suggestions. Do not invent product details. Include review points before expensive generation and before outputs are shared. If direct Jev, Flow, NotebookLM or another connector is unavailable, expose an explicit import/export step; do not simulate the connection. Record which step generated each output, and surface errors without discarding earlier work. Do not publish or share the app publicly.

Sebelum membina workflow, gunakan galeri: periksa semua 22 entri dalam inventori dan apa-apa tambahan yang muncul. Rekod input/output/model yang sebenar. Utamakan Video Marketer, Video Hooks Brainstormer, Product Marketing, Marketing Maven, Social Media Post dan Sticker Generator untuk aliran ini. Baki aplikasi mesti mempunyai catatan kegunaan, ujian atau sebab tidak relevan; jangan claim semua telah digunakan jika hanya dilihat.

## Prompt G7 — AI Studio: eksperimen dan kontrak Google

Evaluate the Google model capabilities available in this account for the supplied campaign brief. Produce structured scripts and scene plans first. Test image generation/editing and video generation only where the UI/account supports them. Record actual model IDs, settings, errors, latency and available usage information. Do not invent API availability based on a web subscription.

For production integration, propose a minimal server-side adapter using current official documentation. Separate credentials from frontend code. Define request/response validation, timeouts, rate-limit handling, job polling if supported, asset persistence, cost limits and an offline/mock test path. Show a runnable example only for an endpoint/model that is documented and accessible. Mark account/billing blockers explicitly. Never output API keys or claim integration without an executed test.

## Prompt G8 — Jev: keputusan berstruktur

Hantar ringkasan minimum yang relevan melalui wrapper sebenar, bukan prompt bebas yang meminta esei. Bentukkan `Choice`, `Score` atau primitive yang benar-benar disokong:

- route: `upload_existing`, `generate_image`, `generate_video`, `revise_script`, `needs_missing_facts`.
- brief_status: `sufficient`, `missing_product_facts`, `missing_reference`, `missing_objective`.
- script_quality: rubric jelas untuk kejelasan, ketepatan fakta, kesesuaian CTA dan durasi anggaran; tidak meramal views.
- revision_action: `accept_for_preview`, `revise_once`, `request_missing_input`.

Validate jawapan, rekod engine dan model jika tersedia, hadkan input, cache berasaskan versi. Jangan menganggap pilihan Jev sebagai kelulusan pengguna untuk transaksi atau perkongsian. Sertakan status failure/fallback yang boleh dibaca pengguna.

---

## Prompt R — Sambung kerja selepas konteks/token habis

Baca `docs/IMPLEMENTATION_STATUS.md`, fail prompt ini dan perubahan kerja terkini. Jangan mengulang kerja yang sudah mempunyai bukti. Sahkan keadaan filesystem/runtime sebelum menyambung. Sambung tugas tertinggi yang belum lulus gate, jalankan ujian khusus bagi risiko yang masih ada, kemudian kemas kini checkpoint.

Checkpoint wajib mengandungi: fasa semasa; fail berubah; keputusan seni bina; command/startup; ujian lulus/gagal; URL projek Google yang perlu disambung tanpa token login; model/usage yang benar-benar diketahui; halangan; tiga langkah seterusnya; perkara yang memerlukan input pengguna. Jangan simpan rahsia atau raw OAuth URL.

## Format laporan akhir ejen

1. Apa yang pengguna kini boleh lakukan.
2. Ciri siap, experimental, blocked dan belum dibuat.
3. Fail/artifak dan cara menjalankan.
4. Bukti ujian serta batasan yang masih material.
5. Penggunaan/kos yang diketahui; tulis tidak diketahui jika tidak tersedia.
6. Langkah seterusnya yang konkrit.

Pintu siap keseluruhan: instalasi boleh ulang, projek boleh disambung, dashboard boleh digunakan, sekurang-kurangnya satu MP4 sah, integrasi yang didakwa mempunyai ujian sebenar, dan dokumentasi sepadan dengan kod. Jika ada gate terhalang, nyatakan tepat; jangan menutupnya dengan istilah SOTA atau status Done.
