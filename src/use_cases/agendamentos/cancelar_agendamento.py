from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.repositories.agendamento_repository import AgendamentoRepository
from src.utils.n8n_webhook import liberar_horario_agendamento


def _horarios_ocupados(horario_inicio: str, horario_fim: str) -> List[str]:
    """Gera a lista de horários de 1h entre início (inclusive) e fim
    (exclusive) — mesmo recorte de slots usado pelo workflow do n8n ao
    criar o agendamento (ver AGENDAMENTO_N8N.md)."""
    inicio_h, inicio_m = (int(parte) for parte in horario_inicio.split(":"))
    fim_h, fim_m = (int(parte) for parte in horario_fim.split(":"))
    minutos_inicio = inicio_h * 60 + inicio_m
    minutos_fim = fim_h * 60 + fim_m

    horarios = []
    minuto_atual = minutos_inicio
    while minuto_atual < minutos_fim:
        horarios.append(f"{minuto_atual // 60:02d}:{minuto_atual % 60:02d}")
        minuto_atual += 60
    return horarios


class CancelarAgendamentoUseCase:
    def __init__(self, db: Session):
        self.agendamento_repository = AgendamentoRepository(db)

    def execute(self, agendamento_id: int):
        agendamento = self.agendamento_repository.get_by_id(agendamento_id)
        if not agendamento:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agendamento não encontrado")
        if agendamento.status == "cancelado":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Agendamento já está cancelado")

        horarios = _horarios_ocupados(agendamento.horario_inicio, agendamento.horario_fim)
        agendamento = self.agendamento_repository.cancelar(agendamento)
        liberar_horario_agendamento(agendamento.data, horarios)
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
