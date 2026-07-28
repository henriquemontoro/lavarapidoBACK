from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.models.user_model import UserRole


@dataclass
class User:
    id: Optional[int] = None
    name: str = ""
    email: str = ""
    hashed_password: str = ""
    is_active: bool = True
    role: UserRole = UserRole.EMPLOYEE
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
