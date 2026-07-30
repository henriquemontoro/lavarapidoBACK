from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.database.database import get_db
from src.middlewares.require_role import require_role
from src.models.user_model import UserModel, UserRole
from src.use_cases.termo.aceitar_termo import AceitarTermoUseCase
from src.use_cases.termo.excluir_resposta_termo import ExcluirRespostaTermoUseCase
from src.use_cases.termo.listar_atendimentos_abertos import ListarAtendimentosAbertosUseCase
from src.use_cases.termo.listar_respostas_termo import ListarRespostasTermoUseCase

router = APIRouter(prefix="/termo", tags=["termo"])


class AtendimentoAbertoResponse(BaseModel):
    atendimento_id: int
    cliente_nome: str
    placa: Optional[str] = None
    modelo_carro: str
    cor_carro: Optional[str] = None
    preco_total: float = 0.0


class AceitarTermoRequest(BaseModel):
    atendimento_id: int
    cpf: str
    tem_plano: bool
    plano: Optional[str] = None


class AceitarTermoResponse(BaseModel):
    atendimento_id: int
    termo_aceito_em: Optional[datetime] = None


class RespostaTermoResponse(BaseModel):
    atendimento_id: int
    cliente_nome: str
    placa: Optional[str] = None
    modelo_carro: Optional[str] = None
    cpf: Optional[str] = None
    tem_plano: bool
    plano: Optional[str] = None
    aceito_em: Optional[datetime] = None


# Rotas públicas (sem autenticação): o cliente acessa o link do termo pelo
# celular, sem estar logado no Portal Nogueira.
@router.get("/atendimentos-abertos", response_model=List[AtendimentoAbertoResponse])
def listar_atendimentos_abertos(db: Session = Depends(get_db)):
    use_case = ListarAtendimentosAbertosUseCase(db)
    return use_case.execute()


@router.post("/aceitar", response_model=AceitarTermoResponse)
def aceitar_termo(request: AceitarTermoRequest, db: Session = Depends(get_db)):
    use_case = AceitarTermoUseCase(db)
    return use_case.execute(request.atendimento_id, request.cpf, request.tem_plano, request.plano)


# Rota protegida: aba do admin/painel pra ver quem respondeu.
@router.get("/respostas", response_model=List[RespostaTermoResponse])
def listar_respostas(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_role(UserRole.OWNER, UserRole.EMPLOYEE)),
):
    use_case = ListarRespostasTermoUseCase(db)
    return use_case.execute()


@router.delete("/respostas/{atendimento_id}", status_code=204)
def excluir_resposta(
    atendimento_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_role(UserRole.OWNER, UserRole.EMPLOYEE)),
):
    use_case = ExcluirRespostaTermoUseCase(db)
    use_case.execute(atendimento_id)
    return Response(status_code=204)
