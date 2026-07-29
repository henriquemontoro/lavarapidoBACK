from sqlalchemy.orm import Session

from src.repositories.atendimento_repository import AtendimentoRepository
from src.repositories.cliente_repository import ClienteRepository
from src.use_cases.clientes.cliente_response import build_cliente_response


class ListClientesUseCase:
    def __init__(self, db: Session):
        self.cliente_repository = ClienteRepository(db)
        self.atendimento_repository = AtendimentoRepository(db)

    def execute(self):
        clientes = self.cliente_repository.list_all()
        atendimentos = self.atendimento_repository.list_all()

        ultimo_por_cliente = {}
        for atendimento in atendimentos:
            atual = ultimo_por_cliente.get(atendimento.cliente_id)
            if atual is None or atendimento.id > atual.id:
                ultimo_por_cliente[atendimento.cliente_id] = atendimento

        return [
            build_cliente_response(cliente, ultimo_por_cliente.get(cliente.id))
            for cliente in clientes
        ]
