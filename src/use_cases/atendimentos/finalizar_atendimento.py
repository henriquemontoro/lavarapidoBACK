from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.models.user_model import UserModel
from src.repositories.atendimento_repository import AtendimentoRepository
from src.repositories.cliente_repository import ClienteRepository
from src.utils.n8n_webhook import notificar_pronto


class FinalizarAtendimentoUseCase:
    def __init__(self, db: Session):
        self.atendimento_repository = AtendimentoRepository(db)
        self.cliente_repository = ClienteRepository(db)

    def execute(self, atendimento_id: int, current_user: UserModel):
        atendimento = self.atendimento_repository.get_by_id(atendimento_id)
        if not atendimento:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atendimento não encontrado")

        if atendimento.finalizado_em is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Atendimento já finalizado")

        atendimento = self.atendimento_repository.finalizar(atendimento_id, current_user.id)

        cliente = self.cliente_repository.get_by_id(atendimento.cliente_id)
        if cliente:
            notificar_pronto(telefone=cliente.telefone, modelo_carro=cliente.modelo_carro)

        return {
            "id": atendimento.id,
            "cliente_id": atendimento.cliente_id,
            "finalizado_em": atendimento.finalizado_em,
        }
