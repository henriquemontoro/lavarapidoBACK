from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.database.database import get_db
from src.middlewares.require_role import require_role
from src.models.user_model import UserModel, UserRole
from src.use_cases.atendimentos.finalizar_atendimento import FinalizarAtendimentoUseCase
from src.use_cases.atendimentos.iniciar_atendimento import (
    IniciarAtendimentoRequest,
    IniciarAtendimentoUseCase,
)

router = APIRouter(prefix="/atendimentos", tags=["atendimentos"])


class AtendimentoResponse(BaseModel):
    id: int
    cliente_id: int
    iniciado_em: Optional[datetime] = None
    finalizado_em: Optional[datetime] = None


@router.post("", response_model=AtendimentoResponse)
def iniciar_atendimento(
    request: IniciarAtendimentoRequest,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_role(UserRole.OWNER, UserRole.EMPLOYEE)),
):
    use_case = IniciarAtendimentoUseCase(db)
    return use_case.execute(request, current_user)


@router.post("/{atendimento_id}/finalizar", response_model=AtendimentoResponse)
def finalizar_atendimento(
    atendimento_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_role(UserRole.OWNER, UserRole.EMPLOYEE)),
):
    use_case = FinalizarAtendimentoUseCase(db)
    return use_case.execute(atendimento_id, current_user)
