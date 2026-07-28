from typing import Literal

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.database import get_db
from src.middlewares.require_role import require_role
from src.models.user_model import UserModel, UserRole
from src.use_cases.dashboard.get_summary import (
    DashboardSummaryResponse,
    GetSummaryRequest,
    GetSummaryUseCase,
)

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummaryResponse)
def get_summary(
    period: Literal["week", "month"] = "week",
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_role(UserRole.OWNER)),
):
    use_case = GetSummaryUseCase(db)
    return use_case.execute(GetSummaryRequest(period=period))
