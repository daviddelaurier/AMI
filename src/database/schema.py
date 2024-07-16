CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_CHAT_HISTORY_TABLE = """
CREATE TABLE IF NOT EXISTS chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_user BOOLEAN NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
"""

CREATE_INDEX_CHAT_HISTORY_USER_ID = """
CREATE INDEX IF NOT EXISTS idx_chat_history_user_id ON chat_history (user_id);
"""

CREATE_INDEX_CHAT_HISTORY_TIMESTAMP = """
CREATE INDEX IF NOT EXISTS idx_chat_history_timestamp ON chat_history (timestamp);
"""
