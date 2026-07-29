from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from src.models.user_model import UserRole
from src.repositories.user_repository import UserRepository
from src.utils.encode_hmac_hash import hash_password


class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole


class CreateUserUseCase:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def execute(self, request: CreateUserRequest):
        if self.repository.get_by_email(request.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email já cadastrado",
            )

        user = self.repository.create(
            name=request.name,
            email=request.email,
            hashed_password=hash_password(request.password),
            role=request.role,
        )
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role.value,
            "is_active": user.is_active,
        }
