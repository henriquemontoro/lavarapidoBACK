from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.repositories.atendimento_repository import AtendimentoRepository
from src.repositories.cliente_repository import ClienteRepository
from src.use_cases.clientes.cliente_response import build_cliente_response


class UpdateClienteRequest(BaseModel):
    nome: str
    sobrenome: str
    telefone: str
    modelo_carro: str


class UpdateClienteUseCase:
    def __init__(self, db: Session):
        self.cliente_repository = ClienteRepository(db)
        self.atendimento_repository = AtendimentoRepository(db)

    def execute(self, cliente_id: int, request: UpdateClienteRequest):
        cliente = self.cliente_repository.update(
            cliente_id,
            nome=request.nome,
            sobrenome=request.sobrenome,
            telefone=request.telefone,
            modelo_carro=request.modelo_carro,
        )
        if not cliente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado")

        ultimo_atendimento = self.atendimento_repository.get_ultimo_by_cliente_id(cliente_id)
        return build_cliente_response(cliente, ultimo_atendimento)
