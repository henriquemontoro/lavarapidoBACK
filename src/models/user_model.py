import enum

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.sql import func

from src.database.database import Base


class UserRole(str, enum.Enum):
    OWNER = "owner"
    EMPLOYEE = "employee"


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    role = Column(
        SQLEnum(UserRole, name="user_role", values_callable=lambda cls: [e.value for e in cls]),
        nullable=False,
        default=UserRole.EMPLOYEE,
    )
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
