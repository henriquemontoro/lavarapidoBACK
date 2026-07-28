from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from src.repositories.user_repository import UserRepository
from src.utils.encode_hmac_hash import hash_password
from src.utils.generate_random_pwd import generate_random_password
from src.utils.send_email import send_email


class ResetPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordUseCase:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def execute(self, request: ResetPasswordRequest):
        user = self.repository.get_by_email(request.email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado",
            )

        new_password = generate_random_password()
        self.repository.update_password(user.id, hash_password(new_password))

        send_email(
            to_email=user.email,
            subject="Redefinição de senha - Lava Rápido",
            body=f"Sua nova senha temporária é: {new_password}",
        )

        return {"detail": "Uma nova senha foi enviada para o seu email"}
