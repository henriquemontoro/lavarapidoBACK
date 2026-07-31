from datetime import date

from sqlalchemy.orm import Session

from src.repositories.agendamento_repository import AgendamentoRepository


class ListarAgendamentosUseCase:
    def __init__(self, db: Session):
        self.agendamento_repository = AgendamentoRepository(db)

    def execute(self):
        hoje = date.today().isoformat()
        agendamentos = self.agendamento_repository.list_a_partir_de(hoje)
        return [
            {
                "id": agendamento.id,
                "nome": agendamento.nome,
                "sobrenome": agendamento.sobrenome,
                "telefone": agendamento.telefone,
                "modelo_carro": agendamento.modelo_carro,
                "placa": agendamento.placa,
                "servicos": agendamento.servicos,
                "preco_total": agendamento.preco_total,
                "data": agendamento.data,
                "horario_inicio": agendamento.horario_inicio,
                "horario_fim": agendamento.horario_fim,
                "status": agendamento.status,
                "criado_em": agendamento.criado_em,
            }
            for agendamento in agendamentos
        ]
