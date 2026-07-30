from sqlalchemy.orm import Session

from src.repositories.atendimento_repository import AtendimentoRepository
from src.repositories.cliente_repository import ClienteRepository


class ListarRespostasTermoUseCase:
    def __init__(self, db: Session):
        self.atendimento_repository = AtendimentoRepository(db)
        self.cliente_repository = ClienteRepository(db)

    def execute(self):
        atendimentos = self.atendimento_repository.list_com_termo_aceito()
        resultado = []
        for atendimento in atendimentos:
            cliente = self.cliente_repository.get_by_id(atendimento.cliente_id)
            resultado.append(
                {
                    "atendimento_id": atendimento.id,
                    "cliente_nome": f"{cliente.nome} {cliente.sobrenome}" if cliente else "Cliente removido",
                    "placa": cliente.placa if cliente else None,
                    "modelo_carro": cliente.modelo_carro if cliente else None,
                    "cpf": atendimento.termo_cpf,
                    "tem_plano": bool(atendimento.termo_tem_plano),
                    "plano": atendimento.termo_plano,
                    "aceito_em": atendimento.termo_aceito_em,
                }
            )
        return resultado
