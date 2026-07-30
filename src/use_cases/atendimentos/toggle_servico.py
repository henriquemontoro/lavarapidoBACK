from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.models.user_model import UserModel
from src.repositories.atendimento_servico_repository import AtendimentoServicoRepository


class ToggleServicoUseCase:
    def __init__(self, db: Session):
        self.servico_repository = AtendimentoServicoRepository(db)

    def execute(self, atendimento_id: int, servico_id: int, concluido: bool, current_user: UserModel):
        item = self.servico_repository.get_by_id(servico_id)
        if not item or item.atendimento_id != atendimento_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Serviço não encontrado")

        return self.servico_repository.set_concluido(servico_id, concluido, current_user.id)
