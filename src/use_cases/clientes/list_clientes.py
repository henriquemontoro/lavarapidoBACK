from sqlalchemy.orm import Session

from src.repositories.atendimento_repository import AtendimentoRepository
from src.repositories.cliente_repository import ClienteRepository
from src.repositories.foto_atendimento_repository import FotoAtendimentoRepository
from src.use_cases.clientes.cliente_response import build_cliente_response


class ListClientesUseCase:
    def __init__(self, db: Session):
        self.cliente_repository = ClienteRepository(db)
        self.atendimento_repository = AtendimentoRepository(db)
        self.foto_repository = FotoAtendimentoRepository(db)

    def execute(self):
        clientes = self.cliente_repository.list_all()
        atendimentos = self.atendimento_repository.list_all()

        ultimo_por_cliente = {}
        for atendimento in atendimentos:
            atual = ultimo_por_cliente.get(atendimento.cliente_id)
            if atual is None or atendimento.id > atual.id:
                ultimo_por_cliente[atendimento.cliente_id] = atendimento

        resultado = []
        for cliente in clientes:
            ultimo_atendimento = ultimo_por_cliente.get(cliente.id)
            foto_counts = (
                self.foto_repository.count_by_atendimento(ultimo_atendimento.id) if ultimo_atendimento else None
            )
            resultado.append(build_cliente_response(cliente, ultimo_atendimento, foto_counts))
        return resultado
