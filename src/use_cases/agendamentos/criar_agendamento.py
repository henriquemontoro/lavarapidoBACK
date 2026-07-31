from typing import List

from sqlalchemy.orm import Session

from src.repositories.agendamento_repository import AgendamentoRepository


class CriarAgendamentoUseCase:
    def __init__(self, db: Session):
        self.agendamento_repository = AgendamentoRepository(db)

    def execute(
        self,
        nome: str,
        sobrenome: str,
        telefone: str,
        modelo_carro: str,
        placa: str,
        servicos: List[str],
        preco_total: float,
        data: str,
        horario_inicio: str,
        horario_fim: str,
    ):
        agendamento = self.agendamento_repository.create(
            nome=nome,
            sobrenome=sobrenome,
            telefone=telefone,
            modelo_carro=modelo_carro,
            placa=placa,
            servicos=servicos,
            preco_total=preco_total,
            data=data,
            horario_inicio=horario_inicio,
            horario_fim=horario_fim,
        )
        return {
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
