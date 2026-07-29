from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.models.user_model import UserModel
from src.repositories.atendimento_repository import AtendimentoRepository
from src.repositories.cliente_repository import ClienteRepository
from src.utils.n8n_webhook import notificar_inicio


class IniciarAtendimentoRequest(BaseModel):
    cliente_id: int


class IniciarAtendimentoUseCase:
    def __init__(self, db: Session):
        self.cliente_repository = ClienteRepository(db)
        self.atendimento_repository = AtendimentoRepository(db)

    def execute(self, request: IniciarAtendimentoRequest, current_user: UserModel):
        cliente = self.cliente_repository.get_by_id(request.cliente_id)
        if not cliente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado")

        if self.atendimento_repository.get_ativo_by_cliente_id(request.cliente_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Esse cliente já tem um atendimento em andamento",
            )

        atendimento = self.atendimento_repository.create(
            cliente_id=request.cliente_id,
            iniciado_por_id=current_user.id,
        )
        notificar_inicio(telefone=cliente.telefone, modelo_carro=cliente.modelo_carro)
        return {
            "id": atendimento.id,
            "cliente_id": atendimento.cliente_id,
            "iniciado_em": atendimento.iniciado_em,
        }
