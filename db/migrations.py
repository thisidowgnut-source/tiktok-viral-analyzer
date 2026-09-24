"""
Schema migrations and initial database initialization for ViralStudio.
"""

import json
from datetime import datetime, timezone
import sqlite3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from db.database import get_db

MIGRATION_V1_SQL = """
CREATE TABLE IF NOT EXISTS schema_migrations (
    version INTEGER PRIMARY KEY,
    applied_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS brand_kits (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    colors TEXT NOT NULL,          -- JSON object of color palette
    logo_font TEXT NOT NULL,       -- JSON object of fonts & logo paths
    language_style TEXT NOT NULL,  -- e.g. 'Santai, bertenaga, viral'
    cta TEXT NOT NULL,             -- default CTA
    product_facts TEXT NOT NULL,   -- JSON array of verified facts
    is_default INTEGER DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS projects (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    language TEXT NOT NULL DEFAULT 'ms',
    brand_kit_id TEXT REFERENCES brand_kits(id) ON DELETE SET NULL,
    brief TEXT NOT NULL,           -- JSON object of brief inputs
    status TEXT NOT NULL DEFAULT 'DRAFT', -- 'DRAFT', 'READY_REVIEW', 'RENDERING', 'COMPLETED'
    version INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS scenes (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    sequence INTEGER NOT NULL,
    script TEXT NOT NULL,
    duration REAL NOT NULL DEFAULT 3.0,
    asset_id TEXT,
    crop_focal_point TEXT NOT NULL DEFAULT 'center',
    transition TEXT NOT NULL DEFAULT 'cut',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS assets (
    id TEXT PRIMARY KEY,
    project_id TEXT REFERENCES projects(id) ON DELETE SET NULL,
    type TEXT NOT NULL,            -- 'video', 'image', 'audio'
    source TEXT NOT NULL,          -- 'upload', 'generated', 'demo'
    internal_path TEXT NOT NULL,
    filename TEXT NOT NULL,
    checksum_sha256 TEXT NOT NULL,
    dimensions TEXT,               -- e.g. '720x1280'
    duration REAL DEFAULT 0.0,
    provenance TEXT,               -- source documentation
    review_status TEXT NOT NULL DEFAULT 'UNREVIEWED', -- 'UNREVIEWED', 'APPROVED', 'REJECTED'
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS jobs (
    id TEXT PRIMARY KEY,
    project_id TEXT REFERENCES projects(id) ON DELETE SET NULL,
    type TEXT NOT NULL,            -- 'render_video', 'tts', 'analysis'
    input_hash TEXT NOT NULL,
    state TEXT NOT NULL DEFAULT 'QUEUED', -- 'QUEUED', 'RUNNING', 'COMPLETED', 'FAILED', 'CANCELLED'
    progress REAL NOT NULL DEFAULT 0.0,
    error_code TEXT,
    error_message TEXT,
    attempts INTEGER NOT NULL DEFAULT 0,
    output_ids TEXT NOT NULL DEFAULT '[]', -- JSON array of generated asset IDs
    cancellation_requested INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS provider_runs (
    id TEXT PRIMARY KEY,
    job_id TEXT REFERENCES jobs(id) ON DELETE CASCADE,
    provider TEXT NOT NULL,        -- 'jev_system_one', 'edge_tts', 'ffmpeg'
    model TEXT NOT NULL,
    prompt_version TEXT,
    rubric_version TEXT,
    latency_ms REAL NOT NULL DEFAULT 0.0,
    usage_tokens INTEGER NOT NULL DEFAULT 0,
    estimated_cost REAL NOT NULL DEFAULT 0.0,
    currency TEXT NOT NULL DEFAULT 'USD',
    created_at TEXT NOT NULL
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_scenes_project_seq ON scenes(project_id, sequence);
CREATE INDEX IF NOT EXISTS idx_assets_checksum ON assets(checksum_sha256);
CREATE INDEX IF NOT EXISTS idx_jobs_state ON jobs(state);
CREATE INDEX IF NOT EXISTS idx_jobs_project ON jobs(project_id);
"""

def seed_default_brand_kit(conn: sqlite3.Connection):
    """Seeds the verified DOH-NUT ground-truth brand kit."""
    now = datetime.now(timezone.utc).isoformat()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM brand_kits WHERE id = 'brand_dohnut_default'")
    if cursor.fetchone():
        return

    colors = {
        "frosting_pink": "#EF9FBD",
        "cream_dough": "#FDEFEB",
        "classic_blue": "#297ABE",
        "navy_dark": "#07334F",
        "butter_yellow": "#FEDE33",
        "truffle_choc": "#2B1408",
    }
    logo_font = {
        "primary_font": "Plus Jakarta Sans, sans-serif",
        "display_font": "Clash Display, sans-serif",
        "logo_path": "/brand/dohnut-logo.png",
    }
    product_facts = [
        {"claim": "Doh-Nut dimiliki oleh GangNiaga Sdn. Bhd.", "verified": True},
        {"claim": "Tagline rasmi: GOOD VIBE. GOOD DOH.", "verified": True},
        {"claim": "Maskot rasmi: DOH BOY™", "verified": True},
        {"claim": "31 Perisa artisan berbeza (Classic, Sprinkled, Stuffed, Savory, Heritage)", "verified": True},
        {"claim": "Ambang penghantaran percuma RM25 ke atas", "verified": True},
        {"claim": "Doh brioche-sourdough difermentasi 48 jam", "verified": True},
    ]

    cursor.execute(
        """
        INSERT INTO brand_kits (id, name, colors, logo_font, language_style, cta, product_facts, is_default, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
        """,
        (
            "brand_dohnut_default",
            "DOH-NUT™ Artisanal Brand Kit",
            json.dumps(colors),
            json.dumps(logo_font),
            "Santai, bertenaga, meme-aware, loghat Melayu moden ('Doh sedap', 'Doh giler')",
            "Tekan beg kuning sekarang untuk order panas-panas!",
            json.dumps(product_facts),
            now,
            now,
        ),
    )

def run_migrations():
    """Runs all pending schema migrations."""
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version INTEGER PRIMARY KEY,
                applied_at TEXT NOT NULL
            );
            """
        )
        cursor = conn.cursor()
        cursor.execute("SELECT version FROM schema_migrations WHERE version = 1")
        row = cursor.fetchone()
        if not row:
            conn.executescript(MIGRATION_V1_SQL)
            seed_default_brand_kit(conn)
            now = datetime.now(timezone.utc).isoformat()
            cursor.execute(
                "INSERT INTO schema_migrations (version, applied_at) VALUES (1, ?)",
                (now,),
            )
            print("[+] Migration v1 applied successfully.")
        else:
            print("[*] Database is up to date (Migration v1).")

if __name__ == "__main__":
    run_migrations()
