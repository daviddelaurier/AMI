from dataclasses import dataclass
from datetime import datetime

@dataclass
class ChatMessage:
    id: int
    user_id: int
    message: str
    timestamp: datetime
    is_user: bool

@dataclass
class User:
    id: int
    username: str
    email: str
    created_at: datetime
