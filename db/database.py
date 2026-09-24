"""
SQLite Database Connection Manager for ViralStudio.
Uses Python's built-in sqlite3 with WAL journal mode and foreign key enforcement.
"""

import sqlite3
import contextlib
from typing import Generator
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app_core.config import DB_PATH

def get_connection() -> sqlite3.Connection:
    """Creates a new configured SQLite connection."""
    conn = sqlite3.connect(str(DB_PATH), timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA busy_timeout = 5000;")
    return conn

@contextlib.contextmanager
def get_db() -> Generator[sqlite3.Connection, None, None]:
    """Context manager for automatic commit and rollback."""
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
