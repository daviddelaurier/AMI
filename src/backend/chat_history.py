from src.database.db import insert_chat_message, get_chat_history, search_chat_history
import csv
from io import StringIO

def save_chat_message(user_id, message, is_user=True):
    insert_chat_message(user_id, message, is_user)

def retrieve_chat_history(user_id, limit=50):
    return get_chat_history(user_id, limit)

def search_messages(user_id, query):
    return search_chat_history(user_id, query)

def export_chat_history(user_id):
    history = get_chat_history(user_id)
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Timestamp', 'Sender', 'Message'])
    for message in history:
        writer.writerow([message['timestamp'], 'User' if message['is_user'] else 'AI', message['message']])
    return output.getvalue()