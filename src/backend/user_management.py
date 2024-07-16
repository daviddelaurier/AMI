from werkzeug.security import generate_password_hash, check_password_hash
from src.database.db import insert_user, get_user_by_username, update_user_profile, get_user_profile

def register_user(username, password):
    hashed_password = generate_password_hash(password)
    insert_user(username, hashed_password)

def authenticate_user(username, password):
    user = get_user_by_username(username)
    if user and check_password_hash(user['password'], password):
        return user
    return None

def update_profile(user_id, name, email, preferences):
    update_user_profile(user_id, name, email, preferences)

def get_profile(user_id):
    return get_user_profile(user_id)