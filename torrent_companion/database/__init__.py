import os
import sqlite3
import logging
from typing import List

from torrent_companion.indexers.base_indexer import BaseIndexer

logger = logging.getLogger(__name__)


class DatabaseHandler:
    def __init__(self):
        self.filepath = os.environ.get("DB_FILEPATH", "/var/profiling/database.db")
        self.conn = sqlite3.connect(self.filepath, check_same_thread=False, timeout=10)

    def __del__(self):
        if self.conn:
            self.conn.close()
    
    def create_table(self, table_name: str, columns: List[str]):
        """Create a table if it does not exist."""
        cursor = self.conn.cursor()
        columns_str = ", ".join(columns)
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})")
        self.conn.commit()
    
    def insert(self, table_name: str, data: dict):
        """Insert data into a table."""
        cursor = self.conn.cursor()
        columns = ", ".join(data.keys())
        placeholders = ", ".join("?" for _ in data)
        cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", tuple(data.values()))
        self.conn.commit()
    
    def table_setup(self):
        """Create necessary tables if they do not exist."""
        self.create_table(
            "uploader_profiles",
            [
                "id INTEGER PRIMARY KEY AUTOINCREMENT",
                "name TEXT NOT NULL",
                "rating FLOAT DEFAULT 0",
                "plataform TEXT DEFAULT 'Any'",
                "total_pages INTEGER DEFAULT 0",
                "total_seeders INTEGER DEFAULT 0",
                "total_leechers INTEGER DEFAULT 0",
                "average_uploads_per_month REAL DEFAULT 0",
                "average_seeders_per_upload REAL DEFAULT 0",
                "recent_activity TEXT",
                "oldest_activity TEXT",
                "fetched_at TEXT"
            ]
        )
        
        self.create_table(
            "best_torrent_cache",
            [
                
            ]
        )