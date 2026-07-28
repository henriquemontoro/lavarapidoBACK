from sqlalchemy.orm import Session

from src.repositories.atendimento_repository import AtendimentoRepository
from src.repositories.cliente_repository import ClienteRepository


class ListClientesUseCase:
    def __init__(self, db: Session):
        self.cliente_repository = ClienteRepository(db)
        self.atendimento_repository = AtendimentoRepository(db)

    def execute(self):
        clientes = self.cliente_repository.list_all()
        atendimentos_ativos = self.atendimento_repository.list_ativos()
        ativo_por_cliente = {a.cliente_id: a for a in atendimentos_ativos}

        resultado = []
        for cliente in clientes:
            atendimento = ativo_por_cliente.get(cliente.id)
            resultado.append(
                {
                    "id": cliente.id,
                    "nome": cliente.nome,
                    "sobrenome": cliente.sobrenome,
                    "telefone": cliente.telefone,
                    "modelo_carro": cliente.modelo_carro,
                    "atendimento_ativo_id": atendimento.id if atendimento else None,
                    "atendimento_iniciado_em": atendimento.iniciado_em if atendimento else None,
                }
            )
        return resultado
