from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.repositories.cliente_repository import ClienteRepository


class CreateClienteRequest(BaseModel):
    nome: str
    sobrenome: str
    telefone: str
    modelo_carro: str


class CreateClienteUseCase:
    def __init__(self, db: Session):
        self.repository = ClienteRepository(db)

    def execute(self, request: CreateClienteRequest):
        cliente = self.repository.create(
            nome=request.nome,
            sobrenome=request.sobrenome,
            telefone=request.telefone,
            modelo_carro=request.modelo_carro,
        )
        return {
            "id": cliente.id,
            "nome": cliente.nome,
            "sobrenome": cliente.sobrenome,
            "telefone": cliente.telefone,
            "modelo_carro": cliente.modelo_carro,
            "atendimento_ativo_id": None,
            "atendimento_iniciado_em": None,
        }
