from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from jose import jwt
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from src.config.config import get_settings
from src.repositories.user_repository import UserRepository
from src.utils.encode_hmac_hash import verify_password

settings = get_settings()


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


class LoginUseCase:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def execute(self, request: LoginRequest):
        user = self.repository.get_by_email(request.email)

        if not user or not verify_password(request.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha inválidos",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuário inativo",
            )

        access_token = create_access_token({"sub": str(user.id)})

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "role": user.role.value,
        }
