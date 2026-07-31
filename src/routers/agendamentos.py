from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.database.database import get_db
from src.middlewares.require_role import require_role
from src.middlewares.validate_webhook_secret import validate_webhook_secret
from src.models.user_model import UserModel, UserRole
from src.use_cases.agendamentos.cancelar_agendamento import CancelarAgendamentoUseCase
from src.use_cases.agendamentos.criar_agendamento import CriarAgendamentoUseCase
from src.use_cases.agendamentos.listar_agendamentos import ListarAgendamentosUseCase

router = APIRouter(prefix="/agendamentos", tags=["agendamentos"])


class AgendamentoCreateRequest(BaseModel):
    nome: str
    sobrenome: str
    telefone: str
    modelo_carro: str
    placa: str
    servicos: List[str]
    preco_total: float
    data: str
    horario_inicio: str
    horario_fim: str


class AgendamentoResponse(BaseModel):
    id: int
    nome: str
    sobrenome: str
    telefone: str
    modelo_carro: str
    placa: Optional[str] = None
    servicos: List[str]
    preco_total: float
    data: str
    horario_inicio: str
    horario_fim: str
    status: str
    criado_em: Optional[datetime] = None


@router.post("", response_model=AgendamentoResponse, dependencies=[Depends(validate_webhook_secret)])
def criar_agendamento(request: AgendamentoCreateRequest, db: Session = Depends(get_db)):
    """Chamado pelo workflow do n8n depois que ele já confirmou o horário
    disponível na Data Table dele. Autenticado por segredo (header
    X-N8N-Secret), não por login de usuário."""
    use_case = CriarAgendamentoUseCase(db)
    return use_case.execute(**request.model_dump())


@router.get("", response_model=List[AgendamentoResponse])
def listar_agendamentos(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_role(UserRole.OWNER, UserRole.EMPLOYEE)),
):
    use_case = ListarAgendamentosUseCase(db)
    return use_case.execute()


@router.patch("/{agendamento_id}/cancelar", response_model=AgendamentoResponse)
def cancelar_agendamento(
    agendamento_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_role(UserRole.OWNER, UserRole.EMPLOYEE)),
):
    """Desmarca um agendamento pelo site. Só muda o status aqui no painel —
    não libera o horário na Data Table do n8n, que é a fonte da verdade da
    agenda usada pelo assistente do WhatsApp."""
    use_case = CancelarAgendamentoUseCase(db)
    return use_case.execute(agendamento_id)
