import sqlite3
from datetime import datetime
import json

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

def get_conversations():
    try:
        conn = sqlite3.connect("memory.db")
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT session_id, message_data, created_at FROM agent_messages ORDER BY session_id, id").fetchall()
        conn.close()
    except sqlite3.OperationalError:
        return {}

    conversations = {}
    for row in rows:
        session_id = row["session_id"]
        data = json.loads(row["message_data"])
        role = data.get("role", "unknown")

        if isinstance(data.get("content"), list):
            text = data["content"][0]["text"] if data["content"] else ""
        else:
            text = data.get("content", "")

        if session_id not in conversations:
            conversations[session_id] = []

        conversations[session_id].append({
            "role": role,
            "content": text,
            "created_at": row["created_at"]
        })

    return conversations