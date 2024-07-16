import sqlite3
from contextlib import contextmanager

DATABASE_NAME = 'artificial_me.db'

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def execute_query(query, params=None):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        return cursor

def fetch_one(query, params=None):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchone()

def fetch_all(query, params=None):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchall()

# Optimized query for retrieving chat history
def get_chat_history(user_id, limit=50):
    query = """
    SELECT * FROM chat_history
    WHERE user_id = ?
    ORDER BY timestamp DESC
    LIMIT ?
    """
    return fetch_all(query, (user_id, limit))

# Optimized query for searching chat history
def search_chat_history(user_id, query):
    search_query = """
    SELECT * FROM chat_history
    WHERE user_id = ? AND message LIKE ?
    ORDER BY timestamp DESC
    """
    return fetch_all(search_query, (user_id, f"%{query}%"))