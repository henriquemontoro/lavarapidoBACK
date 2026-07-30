from typing import Optional

from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.repositories.atendimento_repository import AtendimentoRepository
from src.repositories.cliente_repository import ClienteRepository
from src.repositories.foto_atendimento_repository import FotoAtendimentoRepository
from src.use_cases.clientes.cliente_response import build_cliente_response


class UpdateClienteRequest(BaseModel):
    nome: str
    sobrenome: str
    telefone: str
    modelo_carro: str
    placa: Optional[str] = None


class UpdateClienteUseCase:
    def __init__(self, db: Session):
        self.cliente_repository = ClienteRepository(db)
        self.atendimento_repository = AtendimentoRepository(db)
        self.foto_repository = FotoAtendimentoRepository(db)

    def execute(self, cliente_id: int, request: UpdateClienteRequest):
        cliente = self.cliente_repository.update(
            cliente_id,
            nome=request.nome,
            sobrenome=request.sobrenome,
            telefone=request.telefone,
            modelo_carro=request.modelo_carro,
            placa=request.placa,
        )
        if not cliente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado")

        ultimo_atendimento = self.atendimento_repository.get_ultimo_by_cliente_id(cliente_id)
        foto_counts = (
            self.foto_repository.count_by_atendimento(ultimo_atendimento.id) if ultimo_atendimento else None
        )
        return build_cliente_response(cliente, ultimo_atendimento, foto_counts)
