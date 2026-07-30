from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.repositories.atendimento_repository import AtendimentoRepository


class ExcluirRespostaTermoUseCase:
    def __init__(self, db: Session):
        self.atendimento_repository = AtendimentoRepository(db)

    def execute(self, atendimento_id: int):
        atendimento = self.atendimento_repository.get_by_id(atendimento_id)
        if not atendimento:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atendimento não encontrado")

        self.atendimento_repository.limpar_termo(atendimento_id)
