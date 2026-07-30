from typing import List, Tuple

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.models.foto_atendimento_model import MomentoFoto
from src.models.user_model import UserModel
from src.repositories.atendimento_repository import AtendimentoRepository
from src.repositories.cliente_repository import ClienteRepository
from src.repositories.foto_atendimento_repository import FotoAtendimentoRepository
from src.utils.n8n_webhook import notificar_inicio


class IniciarAtendimentoUseCase:
    def __init__(self, db: Session):
        self.cliente_repository = ClienteRepository(db)
        self.atendimento_repository = AtendimentoRepository(db)
        self.foto_repository = FotoAtendimentoRepository(db)

    def execute(self, cliente_id: int, fotos: List[Tuple[bytes, str]], current_user: UserModel):
        if not fotos:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="É preciso anexar ao menos uma foto para iniciar o atendimento",
            )

        cliente = self.cliente_repository.get_by_id(cliente_id)
        if not cliente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado")

        if self.atendimento_repository.get_ativo_by_cliente_id(cliente_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Esse cliente já tem um atendimento em andamento",
            )

        atendimento = self.atendimento_repository.create(
            cliente_id=cliente_id,
            iniciado_por_id=current_user.id,
        )
        self.foto_repository.create_many(
            atendimento_id=atendimento.id,
            momento=MomentoFoto.INICIO,
            registrada_por_id=current_user.id,
            arquivos=fotos,
        )
        notificar_inicio(telefone=cliente.telefone, modelo_carro=cliente.modelo_carro)
        return {
            "id": atendimento.id,
            "cliente_id": atendimento.cliente_id,
            "iniciado_em": atendimento.iniciado_em,
        }
