import os
import sqlite3
from typing import List

class DBHandler:
    def __init__(self):
        self.filepath = os.environ.get("DB_FILEPATH", "/var/torrent_companion/database.db")
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