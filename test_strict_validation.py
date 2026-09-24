"""
Test validation of Khairul Aming video analysis using TikTokVideoAnalysis strict Pydantic model.
"""

import json
from schema_models import (
    TikTokVideoAnalysis,
    TopicCategory,
    HookType,
    HookAnalysis,
    StructureTag,
    StructureItem,
    PacingSpeed
)

sample_data = {
    "video_id": "KA_001",
    "topic_category": "RESEPI_RAMADAN",
    "hook_analysis": {
        "hook_type": "CRAVING_SENSORY",
        "hook_verbatim": "Hey what's up guys! Hari ini kita start Episod 1 daripada 30 Hari 30 Resepi untuk Ramadan tahun ni, and resipi pertama kita ialah Daging Masak Hitam Berempah yang sangat pekat, juicy dan pecah minyak elok.",
        "word_count": 35,
        "has_signature_catchphrase": True
    },
    "structure_breakdown": [
        {
            "order": 1,
            "tag": "HOOK",
            "text": "Hey what's up guys!"
        },
        {
            "order": 2,
            "tag": "HOOK",
            "text": "Hari ini kita start Episod 1 daripada 30 Hari 30 Resepi untuk Ramadan tahun ni, and resipi pertama kita ialah Daging Masak Hitam Berempah yang sangat pekat, juicy dan pecah minyak elok."
        },
        {
            "order": 3,
            "tag": "SETUP",
            "text": "First sekali kita ambil daging lembu yang dipotong nipis, perap dengan kicap manis, kicap pekat dan sedikit sos tiram selama 30 minit."
        },
        {
            "order": 4,
            "tag": "SETUP",
            "text": "Kemudian kita kisar bawang merah, bawang putih, halia, serai dan cili kering sampai lumat."
        },
        {
            "order": 5,
            "tag": "SETUP",
            "text": "Panaskan minyak dalam kuali, tumis empat sekawan sampai naik bau wangi, lepas tu masukkan bahan kisar tadi dan tumis sampai garing dan terbit minyak."
        },
        {
            "order": 6,
            "tag": "SETUP",
            "text": "Masukkan daging yang kita perap tadi berserta air perapan dia, kacau rata dan biarkan daging masak perlahan dengan api sederhana sampai empuk."
        },
        {
            "order": 7,
            "tag": "PAYOFF",
            "text": "Bila kuah dah mula pekat berkilat, masukkan kerisik, air asam jawa dan gula melaka untuk seimbangkan rasa manis dan pedas."
        },
        {
            "order": 8,
            "tag": "PAYOFF",
            "text": "Tengok kuah dia yang hitam berkilat melekat pada daging ni, aroma dia memang menusuk hidung!"
        },
        {
            "order": 9,
            "tag": "PAYOFF",
            "text": "Bila dicedok atas nasi panas berasap, bismillah..."
        },
        {
            "order": 10,
            "tag": "PAYOFF",
            "text": "rasa rempah dia meresap sampai ke dalam, daging lembut tak liat langsung, memang terangkat habis!"
        },
        {
            "order": 11,
            "tag": "SETUP",
            "text": "Senang je nak buat kan?"
        },
        {
            "order": 12,
            "tag": "PITCH",
            "text": "Jangan lupa save video ni untuk menu berbuka korang nanti, selamat mencuba!"
        }
    ],
    "pacing_speed": "RAPID_FIRE",
    "retention_mechanisms": [
        "Jangkar pendengaran 0.8 saat 'Hey what's up guys' dengan nada ceria.",
        "Potongan visual pantas (~1.5s per cut) berlatarkan bunyi ASMR kuali mendidih.",
        "Visual payoff awal (kuah pekat melekat) sebelum resepi diterangkan.",
        "Reaksi suapan tulen 'bismillah' dan frasa tempatan 'terangkat habis'."
    ],
    "closing_call_to_action": "Jangan lupa save video ni untuk menu berbuka korang nanti, selamat mencuba!",
    "viral_factor_summary": "Menggabungkan ritual bermusim Ramadan dengan sensori nafsu makan (craving). Penerangan langkah yang ringkas mendorong kadar simpanan (Saves) dan perkongsian keluarga yang tinggi."
}

def test_validation():
    validated = TikTokVideoAnalysis.model_validate(sample_data)
    print("[+] Model validation SUCCEEDED!")
    print(f"[+] Video ID: {validated.video_id}")
    print(f"[+] Topic: {validated.topic_category.value}")
    print(f"[+] Hook Type: {validated.hook_analysis.hook_type.value}")
    print(f"[+] Total Sentences Tagged: {len(validated.structure_breakdown)}")
    print(f"[+] Pacing: {validated.pacing_speed.value}")
    
    # Dump back to JSON to verify serialization
    json_out = validated.model_dump_json(indent=2)
    with open("validated_output_sample.json", "w", encoding="utf-8") as f:
        f.write(json_out)
    print("[+] Serialized JSON saved to validated_output_sample.json")

if __name__ == "__main__":
    test_validation()
