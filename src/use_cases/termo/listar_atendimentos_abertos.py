from sqlalchemy.orm import Session

from src.repositories.atendimento_repository import AtendimentoRepository
from src.repositories.cliente_repository import ClienteRepository


class ListarAtendimentosAbertosUseCase:
    def __init__(self, db: Session):
        self.atendimento_repository = AtendimentoRepository(db)
        self.cliente_repository = ClienteRepository(db)

    def execute(self):
        atendimentos = self.atendimento_repository.list_ativos()
        resultado = []
        for atendimento in atendimentos:
            cliente = self.cliente_repository.get_by_id(atendimento.cliente_id)
            if cliente:
                resultado.append(
                    {
                        "atendimento_id": atendimento.id,
                        "cliente_nome": f"{cliente.nome} {cliente.sobrenome}",
                        "placa": cliente.placa,
                        "modelo_carro": cliente.modelo_carro,
                        "cor_carro": cliente.cor_carro,
                    }
                )
        return resultado
