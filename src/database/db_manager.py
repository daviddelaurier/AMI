from src.database.db import execute_query, fetch_one, fetch_all
from src.database.schema import (
    CREATE_USERS_TABLE,
    CREATE_CHAT_HISTORY_TABLE,
    CREATE_INDEX_CHAT_HISTORY_USER_ID,
    CREATE_INDEX_CHAT_HISTORY_TIMESTAMP,
)
from src.database.models import User, ChatMessage

def initialize_database():
    execute_query(CREATE_USERS_TABLE)
    execute_query(CREATE_CHAT_HISTORY_TABLE)
    execute_query(CREATE_INDEX_CHAT_HISTORY_USER_ID)
    execute_query(CREATE_INDEX_CHAT_HISTORY_TIMESTAMP)

def create_user(username: str, email: str) -> User:
    query = "INSERT INTO users (username, email) VALUES (?, ?)"
    user_id = execute_query(query, (username, email)).lastrowid
    return get_user_by_id(user_id)

def get_user_by_id(user_id: int) -> User:
    query = "SELECT * FROM users WHERE id = ?"
    row = fetch_one(query, (user_id,))
    return User(**row) if row else None

def add_chat_message(user_id: int, message: str, is_user: bool) -> ChatMessage:
    query = "INSERT INTO chat_history (user_id, message, is_user) VALUES (?, ?, ?)"
    message_id = execute_query(query, (user_id, message, is_user)).lastrowid
    return get_chat_message_by_id(message_id)

def get_chat_message_by_id(message_id: int) -> ChatMessage:
    query = "SELECT * FROM chat_history WHERE id = ?"
    row = fetch_one(query, (message_id,))
    return ChatMessage(**row) if row else None

def get_user_chat_history(user_id: int, limit: int = 50) -> list[ChatMessage]:
    query = """
    SELECT * FROM chat_history
    WHERE user_id = ?
    ORDER BY timestamp DESC
    LIMIT ?
    """
    rows = fetch_all(query, (user_id, limit))
    return [ChatMessage(**row) for row in rows]

def search_user_chat_history(user_id: int, search_query: str) -> list[ChatMessage]:
    query = """
    SELECT * FROM chat_history
    WHERE user_id = ? AND message LIKE ?
    ORDER BY timestamp DESC
    """
    rows = fetch_all(query, (user_id, f"%{search_query}%"))
    return [ChatMessage(**row) for row in rows]
