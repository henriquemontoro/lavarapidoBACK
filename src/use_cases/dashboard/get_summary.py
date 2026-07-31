from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models.lavagem_model import LavagemModel
from src.use_cases.dashboard.periodo import calcular_intervalo


class GetSummaryRequest(BaseModel):
    ano: int
    period: Literal["week", "month"]
    mes: Optional[int] = None
    semana: Optional[int] = None


class DashboardSummaryResponse(BaseModel):
    period: Literal["week", "month"]
    ano: int
    mes: Optional[int] = None
    semana: Optional[int] = None
    inicio: date
    fim: date
    status: Literal["ok", "no_data"]
    clientes_atendidos: int = 0
    total_lavagens: int = 0
    vendas_total: float = 0.0
    ticket_medio: float = 0.0
    tempo_operacional_medio_min: float = 0.0
    produtividade_media_por_funcionario: float = 0.0
    nps_medio: float = 0.0
    nota_google_media: float = 0.0


class GetSummaryUseCase:
    def __init__(self, db: Session):
        self.db = db

    def execute(self, request: GetSummaryRequest) -> DashboardSummaryResponse:
        inicio, fim = calcular_intervalo(request.ano, request.period, request.mes, request.semana)

        base = self.db.query(LavagemModel).filter(
            LavagemModel.data >= inicio,
            LavagemModel.data <= fim,
        )

        total_lavagens = base.count()
        if total_lavagens == 0:
            return DashboardSummaryResponse(
                period=request.period,
                ano=request.ano,
                mes=request.mes,
                semana=request.semana,
                inicio=inicio,
                fim=fim,
                status="no_data",
            )

        agregados = base.with_entities(
            func.count(func.distinct(LavagemModel.cpf)),
            func.count(func.distinct(LavagemModel.funcionario_lavagem)),
            func.sum(LavagemModel.preco_reais),
            func.avg(LavagemModel.tempo_lavagem_total_min),
            func.avg(LavagemModel.nps_cliente),
            func.avg(LavagemModel.nota_google),
        ).one()
        (
            clientes_distintos,
            funcionarios_distintos,
            vendas_total,
            tempo_medio,
            nps_medio,
            nota_google_media,
        ) = agregados

        vendas_total = float(vendas_total or 0)
        funcionarios_distintos = funcionarios_distintos or 1

        return DashboardSummaryResponse(
            period=request.period,
            ano=request.ano,
            mes=request.mes,
            semana=request.semana,
            inicio=inicio,
            fim=fim,
            status="ok",
            clientes_atendidos=clientes_distintos,
            total_lavagens=total_lavagens,
            vendas_total=round(vendas_total, 2),
            ticket_medio=round(vendas_total / total_lavagens, 2),
            tempo_operacional_medio_min=round(float(tempo_medio or 0), 1),
            produtividade_media_por_funcionario=round(total_lavagens / funcionarios_distintos, 1),
            nps_medio=round(float(nps_medio or 0), 1),
            nota_google_media=round(float(nota_google_media or 0), 2),
        )
