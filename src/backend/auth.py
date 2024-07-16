import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from src.database.db import insert_user, get_user_by_username
import jwt
import datetime

# Load environment variables from .env file
load_dotenv()

# Get SECRET_KEY from environment variables
SECRET_KEY = os.getenv("AUTH_SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("AUTH_SECRET_KEY not set in .env file")

def register_user(username, password):
    hashed_password = generate_password_hash(password)
    insert_user(username, hashed_password)

def authenticate_user(username, password):
    user = get_user_by_username(username)
    if user and check_password_hash(user['password'], password):
        token = generate_token(user['id'])
        return token
    return None

def generate_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Token expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'