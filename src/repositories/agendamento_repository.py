from typing import List, Optional

from sqlalchemy.orm import Session

from src.models.agendamento_model import AgendamentoModel


class AgendamentoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
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
    ) -> AgendamentoModel:
        agendamento = AgendamentoModel(
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
        self.db.add(agendamento)
        self.db.commit()
        self.db.refresh(agendamento)
        return agendamento

    def list_a_partir_de(self, data_minima: str) -> List[AgendamentoModel]:
        return (
            self.db.query(AgendamentoModel)
            .filter(AgendamentoModel.data >= data_minima)
            .order_by(AgendamentoModel.data.asc(), AgendamentoModel.horario_inicio.asc())
            .all()
        )

    def get_by_id(self, agendamento_id: int) -> Optional[AgendamentoModel]:
        return self.db.query(AgendamentoModel).filter(AgendamentoModel.id == agendamento_id).first()

    def cancelar(self, agendamento: AgendamentoModel) -> AgendamentoModel:
        agendamento.status = "cancelado"
        self.db.commit()
        self.db.refresh(agendamento)
        return agendamento
