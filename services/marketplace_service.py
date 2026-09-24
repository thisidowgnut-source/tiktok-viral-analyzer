"""
Marketplace & Plugins Service for ViralStudio.
Provides ChatGPT & Claude-style plugins catalog, installation state management,
configuration storage, and plugin execution runtime.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any, Optional

from app_core.config import DATA_DIR

PLUGINS_FILE = DATA_DIR / "plugins_state.json"

DEFAULT_PLUGINS = [
    {
        "id": "plugin_tiktok_shop",
        "name": "TikTok Shop Direct Syncer",
        "category": "E-Dagang",
        "icon": "🛍️",
        "author": "ByteDance Partner SDK",
        "version": "v2.4.0",
        "rating": 4.9,
        "installs": "48.2k",
        "verified": True,
        "description": "Menyegerakkan katalog produk TikTok Shop, harga diskaun promosi, stok langsung, dan link beg kuning terus ke dalam skrip video.",
        "features": [
            "Sinkronisasi harga promosi automatik",
            "Penyuntikan CTA 'Beg Kuning' berpenukaran tinggi",
            "Notifikasi stok habis semasa penjanaan skrip"
        ],
        "installed": True,
        "enabled": True,
        "config": {"shop_id": "SHOP_MY_994821", "auto_sync": True}
    },
    {
        "id": "plugin_elevenlabs",
        "name": "ElevenLabs SOTA Voice Engine",
        "category": "Audio & Suara",
        "icon": "🎙️",
        "author": "ElevenLabs Inc.",
        "version": "v3.1.2",
        "rating": 4.95,
        "installs": "120.5k",
        "verified": True,
        "description": "Kloning suara pencipta dan 30+ pilihan suara hyper-realistic ekspresif dengan intonasi emosi tempatan (Melayu & Manglish).",
        "features": [
            "Voice cloning suara Khairul Aming & Chef Wan",
            "Kawalan kestabilan & ekspresi emosi",
            "Penjanaan audio 24-bit 48kHz lossless"
        ],
        "installed": True,
        "enabled": True,
        "config": {"model": "eleven_multilingual_v2", "stability": 0.75}
    },
    {
        "id": "plugin_capcut",
        "name": "CapCut Project Exporter",
        "category": "Video & Imej",
        "icon": "✂️",
        "author": "CapCut Creative Hub",
        "version": "v1.8.4",
        "rating": 4.85,
        "installs": "95.1k",
        "verified": True,
        "description": "Mengeksport draf timeline CapCut (.draft) dengan potongan babak, sari kata dinamik, dan penanda rentak muzik secara automatik.",
        "features": [
            "Eksport draf CapCut PC dan Mobile terus",
            "Penanda beat muzik untuk transisi tepat",
            "Import klip B-roll ke track sekunder"
        ],
        "installed": True,
        "enabled": True,
        "config": {"export_format": "draft_json", "include_subtitles": True}
    },
    {
        "id": "plugin_whisper",
        "name": "Whisper Kinetic Subtitles AI",
        "category": "Audio & Suara",
        "icon": "💬",
        "author": "OpenAI / SOTA Subtitles",
        "version": "v2.0.1",
        "rating": 4.9,
        "installs": "76.4k",
        "verified": True,
        "description": "Menjana sari kata gaya TikTok & Instagram Reels dengan warna serlahan (karaoke highlight) berasaskan penjajaran paras perkataan.",
        "features": [
            "Word-level timestamp synchronization",
            "Gaya teks neon, pop-in, dan border hitam tebal",
            "Sokongan slanga Melayu dan dialek tempatan"
        ],
        "installed": True,
        "enabled": True,
        "config": {"highlight_color": "#FACC15", "max_words_per_line": 4}
    },
    {
        "id": "plugin_midjourney",
        "name": "Flux & Midjourney B-Roll Generator",
        "category": "Video & Imej",
        "icon": "🎨",
        "author": "Generative Media Lab",
        "version": "v2.2.0",
        "rating": 4.8,
        "installs": "63.8k",
        "verified": True,
        "description": "Menjana imej fotorealistik 9:16 untuk B-roll makanan, close-up lava meleleh, dan pembungkusan produk terus dari babak skrip.",
        "features": [
            "Nisbah aspek 9:16 menegak asli",
            "Pencahayaan dramatik studio makanan",
            "Prompt automatik berasaskan sensory cues"
        ],
        "installed": False,
        "enabled": False,
        "config": {"quality": "ultra", "aspect_ratio": "9:16"}
    },
    {
        "id": "plugin_seo_radar",
        "name": "TikTok Trend & SEO Radar",
        "category": "Penyelidikan & SEO",
        "icon": "📡",
        "author": "ViralGrowth AI",
        "version": "v3.0.0",
        "rating": 4.92,
        "installs": "84.3k",
        "verified": True,
        "description": "Mengimbas kata kunci carian TikTok Search terkini, audio lagu trending di Malaysia, dan kadar lonjakan hashtag #ResepiViral.",
        "features": [
            "Pengesanan 100 audio paling viral di Malaysia",
            "Ramalan kedudukan carian TikTok SEO",
            "Cadangan hashtag berdaya saing rendah tapi volum tinggi"
        ],
        "installed": True,
        "enabled": True,
        "config": {"region": "MY", "category": "Food & Beverage"}
    },
    {
        "id": "plugin_canva",
        "name": "Canva Brand Kit Synchronizer",
        "category": "Video & Imej",
        "icon": "📐",
        "author": "Canva Connect",
        "version": "v1.4.2",
        "rating": 4.75,
        "installs": "52.0k",
        "verified": True,
        "description": "Menghubungkan fail logo, warna jenama rasmi Doh-Nut, dan tipografi terus daripada Canva Enterprise Team.",
        "features": [
            "Penyelarasan palet warna jenama automatik",
            "Import aset SVG logo dan maskot Doh Boy",
            "Eksport thumbnail video terus ke Canva"
        ],
        "installed": False,
        "enabled": False,
        "config": {"team_id": "team_dohnut_brand"}
    },
    {
        "id": "plugin_shopify",
        "name": "Shopify Live Inventory & Orders",
        "category": "E-Dagang",
        "icon": "🛒",
        "author": "Shopify Developers",
        "version": "v2.1.0",
        "rating": 4.88,
        "installs": "41.6k",
        "verified": True,
        "description": "Memaparkan kiraan stok langsung, jumlah pesanan hari ini, dan menjana kupon diskaun unik untuk penonton video TikTok.",
        "features": [
            "Pembuatan kod kupon dinamik (cth: DOHNUT10)",
            "Kiraan stok langsung untuk urgensi 'Tinggal 12 box sahaja!'",
            "Webhook pesanan masuk masa nyata"
        ],
        "installed": False,
        "enabled": False,
        "config": {"shop_domain": "dohnut-bakery.myshopify.com"}
    }
]


class MarketplaceService:
    @classmethod
    def _load_plugins(cls) -> List[Dict[str, Any]]:
        if not PLUGINS_FILE.exists():
            cls._save_plugins(DEFAULT_PLUGINS)
            return DEFAULT_PLUGINS
        try:
            with open(PLUGINS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_PLUGINS

    @classmethod
    def _save_plugins(cls, plugins: List[Dict[str, Any]]) -> None:
        try:
            PLUGINS_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(PLUGINS_FILE, "w", encoding="utf-8") as f:
                json.dump(plugins, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[!] Warning: Could not save plugins: {e}")

    @classmethod
    def list_plugins(cls, category: Optional[str] = None) -> List[Dict[str, Any]]:
        plugins = cls._load_plugins()
        if category and category != "Semua":
            plugins = [p for p in plugins if p.get("category") == category]
        return plugins

    @classmethod
    def toggle_plugin(cls, plugin_id: str) -> Dict[str, Any]:
        plugins = cls._load_plugins()
        target = None
        for p in plugins:
            if p["id"] == plugin_id:
                if not p.get("installed"):
                    p["installed"] = True
                    p["enabled"] = True
                else:
                    p["enabled"] = not p.get("enabled", False)
                target = p
                break
        if target:
            cls._save_plugins(plugins)
            return {"status": "success", "plugin": target}
        raise ValueError(f"Plugin {plugin_id} not found")

    @classmethod
    def uninstall_plugin(cls, plugin_id: str) -> Dict[str, Any]:
        plugins = cls._load_plugins()
        target = None
        for p in plugins:
            if p["id"] == plugin_id:
                p["installed"] = False
                p["enabled"] = False
                target = p
                break
        if target:
            cls._save_plugins(plugins)
            return {"status": "success", "plugin": target}
        raise ValueError(f"Plugin {plugin_id} not found")

    @classmethod
    def configure_plugin(cls, plugin_id: str, config: Dict[str, Any]) -> Dict[str, Any]:
        plugins = cls._load_plugins()
        target = None
        for p in plugins:
            if p["id"] == plugin_id:
                p.setdefault("config", {}).update(config)
                target = p
                break
        if target:
            cls._save_plugins(plugins)
            return {"status": "success", "plugin": target}
        raise ValueError(f"Plugin {plugin_id} not found")

    @classmethod
    def execute_plugin(cls, plugin_id: str, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Simulates/executes live plugin capabilities with rich empirical output."""
        plugins = {p["id"]: p for p in cls._load_plugins()}
        if plugin_id not in plugins:
            raise ValueError(f"Plugin {plugin_id} tidak ditemui.")
        
        p = plugins[plugin_id]
        if not p.get("enabled"):
            raise ValueError(f"Plugin {p['name']} belum diaktifkan. Sila pasang atau hidupkan dahulu.")

        if plugin_id == "plugin_tiktok_shop":
            return {
                "plugin": p["name"],
                "action": action or "sync_products",
                "result": {
                    "synced_products": [
                        {"name": "Doh-Nut Nutella Lava (Box of 4)", "price": "RM 20.80", "stock": 142, "yellow_bag_link": "https://shop.tiktok.com/p/dohnut-nutella"},
                        {"name": "Doh-Nut Sambal Nyet Brioche Burger", "price": "RM 16.90", "stock": 88, "yellow_bag_link": "https://shop.tiktok.com/p/dohnut-sambal"},
                        {"name": "Doh-Nut Matcha Uji Glaze (Box of 6)", "price": "RM 28.50", "stock": 65, "yellow_bag_link": "https://shop.tiktok.com/p/dohnut-matcha"}
                    ],
                    "status": "LIVE_SYNC_OK",
                    "currency": "MYR"
                }
            }
        elif plugin_id == "plugin_seo_radar":
            return {
                "plugin": p["name"],
                "action": action or "scan_trends",
                "result": {
                    "trending_keywords": ["#ResepiViralTikTok", "#KhairulAmingInspo", "#DohNutViral", "#MakanLokalMY", "#SourdoughCraze"],
                    "rising_audio": "Khairul Aming - Intro Melodi Cerita Ramadan (Trending #1 MY)",
                    "search_volume_index": 98.4,
                    "recommended_tags": ["#tiktokmalaysia", "#foodie", "#klfoodie", "#dohnutmy", "#asmrsound"]
                }
            }
        elif plugin_id == "plugin_elevenlabs":
            return {
                "plugin": p["name"],
                "action": action or "clone_preview",
                "result": {
                    "voices_available": ["Khairul Aming AI Neural", "Yasmin Cheerful", "Farhan Energetic", "Adam Narrative"],
                    "active_voice": "Khairul Aming AI Neural",
                    "sample_rate": "48000Hz Lossless",
                    "latency_ms": 115
                }
            }
        elif plugin_id == "plugin_whisper":
            return {
                "plugin": p["name"],
                "action": action or "preview_subtitles",
                "result": {
                    "style": "TikTok Pop-In Karaoke",
                    "words_aligned": 42,
                    "accuracy": "99.4%",
                    "highlight_active": "#FACC15"
                }
            }
        else:
            return {
                "plugin": p["name"],
                "action": action or "generic_exec",
                "result": {"status": "SUCCESS", "message": f"Plugin {p['name']} berjaya memproses tugasan dengan parameter: {params}"}
            }
