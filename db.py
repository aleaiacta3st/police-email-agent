import sqlite3
from datetime import datetime

DB_FILE = "cases.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tool_actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id TEXT,
            timestamp TEXT,
            tool_name TEXT,
            details TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_action(case_id, tool_name, details):
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        "INSERT INTO tool_actions (case_id, timestamp, tool_name, details) VALUES (?, ?, ?, ?)",
        (case_id, datetime.now().isoformat(), tool_name, details)
    )
    conn.commit()
    conn.close()

def get_actions():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM tool_actions ORDER BY timestamp DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]

init_db()