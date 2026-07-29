from typing import Optional

from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from src.models.user_model import UserModel, UserRole
from src.repositories.user_repository import UserRepository
from src.utils.encode_hmac_hash import hash_password


class UpdateUserRequest(BaseModel):
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool
    password: Optional[str] = None


class UpdateUserUseCase:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def execute(self, user_id: int, request: UpdateUserRequest, current_user: UserModel):
        existing_with_email = self.repository.get_by_email(request.email)
        if existing_with_email and existing_with_email.id != user_id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email já cadastrado")

        if user_id == current_user.id and (request.role != UserRole.OWNER or not request.is_active):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Você não pode remover seu próprio acesso de dono",
            )

        user = self.repository.update(
            user_id,
            name=request.name,
            email=request.email,
            role=request.role,
            is_active=request.is_active,
        )
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

        if request.password:
            user = self.repository.update_password(user_id, hash_password(request.password))

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role.value,
            "is_active": user.is_active,
        }
