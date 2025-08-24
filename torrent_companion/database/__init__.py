import logging

from torrent_companion.database.handler import DBHandler

logger = logging.getLogger(__name__)


class Database:
    def __init__(self):
        self.handler = DBHandler()
        
        self.setup_tables()
        
    def setup_tables(self):
        self.handler.create_table(
            "uploaders",
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
        
        self.handler.create_table(
            "torrents",
            [
                "id INTEGER PRIMARY KEY AUTOINCREMENT",
                "uploader_id INTEGER NOT NULL REFERENCES uploaders(id) ON DELETE CASCADE",
                "content_type TEXT NOT NULL CHECK (content_type IN ('movie','episode'))",
                "keywords TEXT NOT NULL",
                "title TEXT NOT NULL",
                "info_hash TEXT NOT NULL UNIQUE",
                "size INTEGER NOT NULL",
                "source TEXT DEFAULT 'Unknown'",
                "quality TEXT DEFAULT 'Unknown'",
                "language TEXT DEFAULT 'Unknown'",
                "episode_number INTEGER",
                "season_number INTEGER",
                "added_date TEXT NOT NULL",
                "magnet_url TEXT NOT NULL",
                "scrapped_at TEXT NOT NULL",
            ]
        )