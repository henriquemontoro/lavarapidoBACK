from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.repositories.atendimento_repository import AtendimentoRepository

PLANOS_VALIDOS = ["Bronze", "Prata", "Ouro"]


class AceitarTermoUseCase:
    def __init__(self, db: Session):
        self.atendimento_repository = AtendimentoRepository(db)

    def execute(self, atendimento_id: int, cpf: str, tem_plano: bool, plano: Optional[str]):
        if not cpf or not cpf.strip():
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Informe o CPF")

        if tem_plano and plano not in PLANOS_VALIDOS:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Selecione um plano válido")

        atendimento = self.atendimento_repository.get_by_id(atendimento_id)
        if not atendimento:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atendimento não encontrado")

        if atendimento.finalizado_em is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Esse atendimento já foi finalizado")

        atendimento = self.atendimento_repository.aceitar_termo(
            atendimento_id,
            cpf=cpf.strip(),
            tem_plano=tem_plano,
            plano=plano if tem_plano else None,
        )
        return {"atendimento_id": atendimento.id, "termo_aceito_em": atendimento.termo_aceito_em}
