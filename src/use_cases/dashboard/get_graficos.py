from datetime import date
from typing import List, Literal, Optional

from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models.lavagem_model import LavagemModel
from src.use_cases.dashboard.periodo import calcular_intervalo

ETAPAS = [
    ("t_teto_vidros_min", "Teto e vidros"),
    ("t_capo_parabrisa_min", "Capô e parabrisa"),
    ("t_laterais_portas_min", "Laterais e portas"),
    ("t_traseira_min", "Traseira"),
    ("t_rodas_pneus_min", "Rodas e pneus"),
    ("t_interior_min", "Interior"),
]

ORDEM_DIAS = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]


class GetGraficosRequest(BaseModel):
    ano: int
    period: Literal["week", "month"]
    mes: Optional[int] = None
    semana: Optional[int] = None


class PontoTendencia(BaseModel):
    data: date
    vendas: float
    lavagens: int


class PontoSatisfacao(BaseModel):
    data: date
    nps_medio: float
    nota_google_media: float


class Contagem(BaseModel):
    chave: str
    quantidade: int


class TempoEtapa(BaseModel):
    etapa: str
    minutos_medios: float


class GraficosResponse(BaseModel):
    tendencia: List[PontoTendencia]
    tempo_por_etapa: List[TempoEtapa]
    metodo_pagamento: List[Contagem]
    produtividade_funcionario: List[Contagem]
    tipo_carro: List[Contagem]
    satisfacao_tendencia: List[PontoSatisfacao]
    volume_dia_semana: List[Contagem]


class GetGraficosUseCase:
    def __init__(self, db: Session):
        self.db = db

    def execute(self, request: GetGraficosRequest) -> GraficosResponse:
        inicio, fim = calcular_intervalo(request.ano, request.period, request.mes, request.semana)

        def base():
            return self.db.query(LavagemModel).filter(
                LavagemModel.data >= inicio,
                LavagemModel.data <= fim,
            )

        tendencia_rows = (
            base()
            .with_entities(
                LavagemModel.data,
                func.sum(LavagemModel.preco_reais),
                func.count(LavagemModel.id_lavagem),
            )
            .group_by(LavagemModel.data)
            .order_by(LavagemModel.data)
            .all()
        )
        tendencia = [
            PontoTendencia(data=data_ref, vendas=round(float(vendas or 0), 2), lavagens=lavagens)
            for data_ref, vendas, lavagens in tendencia_rows
        ]

        tempo_por_etapa = []
        etapas_row = base().with_entities(*[func.avg(getattr(LavagemModel, coluna)) for coluna, _ in ETAPAS]).one()
        for (coluna, rotulo), media in zip(ETAPAS, etapas_row):
            tempo_por_etapa.append(TempoEtapa(etapa=rotulo, minutos_medios=round(float(media or 0), 1)))

        metodo_pagamento_rows = (
            base()
            .with_entities(LavagemModel.metodo_pagamento, func.count(LavagemModel.id_lavagem))
            .group_by(LavagemModel.metodo_pagamento)
            .order_by(func.count(LavagemModel.id_lavagem).desc())
            .all()
        )
        metodo_pagamento = [Contagem(chave=chave, quantidade=quantidade) for chave, quantidade in metodo_pagamento_rows]

        produtividade_rows = (
            base()
            .with_entities(LavagemModel.funcionario_lavagem, func.count(LavagemModel.id_lavagem))
            .group_by(LavagemModel.funcionario_lavagem)
            .order_by(func.count(LavagemModel.id_lavagem).desc())
            .all()
        )
        produtividade_funcionario = [
            Contagem(chave=chave, quantidade=quantidade) for chave, quantidade in produtividade_rows
        ]

        tipo_carro_rows = (
            base()
            .with_entities(LavagemModel.tipo_carro, func.count(LavagemModel.id_lavagem))
            .group_by(LavagemModel.tipo_carro)
            .order_by(func.count(LavagemModel.id_lavagem).desc())
            .all()
        )
        tipo_carro = [Contagem(chave=chave, quantidade=quantidade) for chave, quantidade in tipo_carro_rows]

        satisfacao_rows = (
            base()
            .with_entities(
                LavagemModel.data,
                func.avg(LavagemModel.nps_cliente),
                func.avg(LavagemModel.nota_google),
            )
            .group_by(LavagemModel.data)
            .order_by(LavagemModel.data)
            .all()
        )
        satisfacao_tendencia = [
            PontoSatisfacao(
                data=data_ref,
                nps_medio=round(float(nps or 0), 1),
                nota_google_media=round(float(nota or 0), 2),
            )
            for data_ref, nps, nota in satisfacao_rows
        ]

        dia_semana_rows = (
            base()
            .with_entities(LavagemModel.dia_semana, func.count(LavagemModel.id_lavagem))
            .group_by(LavagemModel.dia_semana)
            .all()
        )
        contagem_por_dia = {chave: quantidade for chave, quantidade in dia_semana_rows}
        volume_dia_semana = [
            Contagem(chave=dia, quantidade=contagem_por_dia.get(dia, 0))
            for dia in ORDEM_DIAS
            if dia in contagem_por_dia
        ]

        return GraficosResponse(
            tendencia=tendencia,
            tempo_por_etapa=tempo_por_etapa,
            metodo_pagamento=metodo_pagamento,
            produtividade_funcionario=produtividade_funcionario,
            tipo_carro=tipo_carro,
            satisfacao_tendencia=satisfacao_tendencia,
            volume_dia_semana=volume_dia_semana,
        )
