"""
Database Connection Management

Provides SQLite connection pooling and initialization.
"""

import sqlite3
from pathlib import Path
from typing import Optional
import threading


# Database path
DB_DIR = Path(__file__).parent.parent.parent / "data"
DB_DIR.mkdir(exist_ok=True)
DB_PATH = DB_DIR / "kuasaturbo.db"

# Thread-local storage for connections
_thread_local = threading.local()


def get_db_connection() -> sqlite3.Connection:
    """
    Get database connection for current thread
    
    Returns:
        SQLite connection with row factory enabled
    """
    if not hasattr(_thread_local, 'connection'):
        conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        conn.row_factory = sqlite3.Row
        _thread_local.connection = conn
    
    return _thread_local.connection


def init_database():
    """
    Initialize database with schema
    
    Creates all required tables if they don't exist.
    """
    from .schema import create_tables
    
    conn = get_db_connection()
    create_tables(conn)
    conn.commit()
    
    print(f"[Database] Initialized at {DB_PATH}")


def close_connection():
    """Close database connection for current thread"""
    if hasattr(_thread_local, 'connection'):
        _thread_local.connection.close()
        delattr(_thread_local, 'connection')
