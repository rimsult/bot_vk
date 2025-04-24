import sqlite3
import os
from threading import Lock
from logger import logger

# Save DB next to this file
DB_PATH = os.path.join(os.path.dirname(__file__), "bot_data.db")

class Storage:
    _lock = Lock()

    def __init__(self):
        with self._lock:
            logger.info(f"Connecting to database at {DB_PATH}")
            self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
            self._init_db()

    def _init_db(self):
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                message TEXT,
                response TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.commit()

    def add_record(self, user_id, message, response):
        logger.debug(f"Inserting into history: {user_id}, {message}, {response}")
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO history (user_id, message, response) VALUES (?, ?, ?)",
            (user_id, message, response)
        )
        self.conn.commit()

    def get_history(self, user_id):
        cur = self.conn.cursor()
        cur.execute(
            "SELECT message, response, timestamp FROM history WHERE user_id=? ORDER BY id DESC LIMIT 50",
            (user_id,)
        )
        rows = cur.fetchall()
        logger.debug(f"Fetched history for {user_id}: {rows}")
        return rows