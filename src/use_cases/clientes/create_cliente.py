from typing import Optional

from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.repositories.cliente_repository import ClienteRepository
from src.use_cases.clientes.cliente_response import build_cliente_response


class CreateClienteRequest(BaseModel):
    nome: str
    sobrenome: str
    telefone: str
    modelo_carro: str
    placa: Optional[str] = None


class CreateClienteUseCase:
    def __init__(self, db: Session):
        self.repository = ClienteRepository(db)

    def execute(self, request: CreateClienteRequest):
        cliente = self.repository.create(
            nome=request.nome,
            sobrenome=request.sobrenome,
            telefone=request.telefone,
            modelo_carro=request.modelo_carro,
            placa=request.placa,
        )
        return build_cliente_response(cliente, ultimo_atendimento=None)
