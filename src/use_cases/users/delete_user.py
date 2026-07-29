from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.models.user_model import UserModel
from src.repositories.user_repository import UserRepository


class DeleteUserUseCase:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def execute(self, user_id: int, current_user: UserModel):
        if user_id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Você não pode excluir a própria conta",
            )

        if not self.repository.get_by_id(user_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

        self.repository.delete(user_id)
