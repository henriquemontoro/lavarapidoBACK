from typing import Literal, Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from src.database.database import get_db
from src.middlewares.require_role import require_role
from src.models.user_model import UserModel, UserRole
from src.use_cases.dashboard.get_graficos import GetGraficosRequest, GetGraficosUseCase, GraficosResponse
from src.use_cases.dashboard.get_periodos_disponiveis import (
    AnosDisponiveisResponse,
    GetPeriodosDisponiveisUseCase,
    PeriodosDisponiveisResponse,
)
from src.use_cases.dashboard.get_summary import (
    DashboardSummaryResponse,
    GetSummaryRequest,
    GetSummaryUseCase,
)
from src.use_cases.dashboard.importar_planilha import ImportarPlanilhaResponse, ImportarPlanilhaUseCase

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/anos", response_model=AnosDisponiveisResponse)
def get_anos(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_role(UserRole.OWNER, UserRole.EMPLOYEE)),
):
    return GetPeriodosDisponiveisUseCase(db).anos()


@router.get("/periodos", response_model=PeriodosDisponiveisResponse)
def get_periodos(
    ano: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_role(UserRole.OWNER, UserRole.EMPLOYEE)),
):
    return GetPeriodosDisponiveisUseCase(db).periodos_do_ano(ano)


@router.get("/summary", response_model=DashboardSummaryResponse)
def get_summary(
    ano: int,
    period: Literal["week", "month"] = "week",
    mes: Optional[int] = None,
    semana: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_role(UserRole.OWNER, UserRole.EMPLOYEE)),
):
    use_case = GetSummaryUseCase(db)
    try:
        return use_case.execute(GetSummaryRequest(ano=ano, period=period, mes=mes, semana=semana))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/graficos", response_model=GraficosResponse)
def get_graficos(
    ano: int,
    period: Literal["week", "month"] = "week",
    mes: Optional[int] = None,
    semana: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_role(UserRole.OWNER, UserRole.EMPLOYEE)),
):
    use_case = GetGraficosUseCase(db)
    try:
        return use_case.execute(GetGraficosRequest(ano=ano, period=period, mes=mes, semana=semana))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/importar", response_model=ImportarPlanilhaResponse)
async def importar_planilha(
    arquivo: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_role(UserRole.OWNER)),
):
    if not arquivo.filename.lower().endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Envie um arquivo .xlsx")

    conteudo = await arquivo.read()
    use_case = ImportarPlanilhaUseCase(db)
    try:
        return use_case.execute(conteudo)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
