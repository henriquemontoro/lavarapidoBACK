from typing import List

from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.repositories.lavagem_repository import LavagemRepository


class AnosDisponiveisResponse(BaseModel):
    anos: List[int]


class PeriodosDisponiveisResponse(BaseModel):
    meses: List[int]
    semanas: List[int]


class GetPeriodosDisponiveisUseCase:
    def __init__(self, db: Session):
        self.repository = LavagemRepository(db)

    def anos(self) -> AnosDisponiveisResponse:
        return AnosDisponiveisResponse(anos=self.repository.anos_disponiveis())

    def periodos_do_ano(self, ano: int) -> PeriodosDisponiveisResponse:
        return PeriodosDisponiveisResponse(
            meses=self.repository.meses_disponiveis(ano),
            semanas=self.repository.semanas_iso_disponiveis(ano),
        )
