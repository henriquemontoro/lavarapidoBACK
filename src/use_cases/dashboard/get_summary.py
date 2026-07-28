from typing import Literal, Optional

from pydantic import BaseModel
from sqlalchemy.orm import Session


class GetSummaryRequest(BaseModel):
    period: Literal["week", "month"]


class DashboardSummaryResponse(BaseModel):
    period: Literal["week", "month"]
    status: Literal["no_data"]
    clients_served: Optional[int] = None
    sales: Optional[float] = None
    operational_times: Optional[dict] = None
    productivity: Optional[dict] = None
    satisfaction: Optional[float] = None


class GetSummaryUseCase:
    def __init__(self, db: Session):
        self.db = db

    def execute(self, request: GetSummaryRequest) -> DashboardSummaryResponse:
        # Aguardando integração com a base de dados tratada (planilha/DB).
        # Assim que a fonte de dados existir, esse use case passa a consultar
        # o repositório real e trocar status="no_data" por status="ok",
        # populando os campos abaixo sem exigir mudança no contrato de resposta.
        return DashboardSummaryResponse(period=request.period, status="no_data")
