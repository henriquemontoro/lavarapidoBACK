from datetime import datetime
from typing import List, Literal, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.database.database import get_db
from src.middlewares.require_role import require_role
from src.models.user_model import UserModel, UserRole
from src.use_cases.clientes.create_cliente import CreateClienteRequest, CreateClienteUseCase
from src.use_cases.clientes.delete_cliente import DeleteClienteUseCase
from src.use_cases.clientes.list_clientes import ListClientesUseCase
from src.use_cases.clientes.update_cliente import UpdateClienteRequest, UpdateClienteUseCase

router = APIRouter(prefix="/clientes", tags=["clientes"])


class ServicoStatusResponse(BaseModel):
    id: int
    servico: str
    concluido: bool
    concluido_em: Optional[datetime] = None


class ClienteResponse(BaseModel):
    id: int
    nome: str
    sobrenome: str
    telefone: str
    modelo_carro: str
    placa: Optional[str] = None
    cor_carro: Optional[str] = None
    servicos: List[str] = []
    status: Literal["aguardando", "em_andamento", "finalizado"]
    atendimento_ativo_id: Optional[int] = None
    atendimento_iniciado_em: Optional[datetime] = None
    atendimento_finalizado_em: Optional[datetime] = None
    termo_aceito: bool = False
    ultimo_atendimento_id: Optional[int] = None
    fotos_inicio_count: int = 0
    fotos_fim_count: int = 0
    servicos_status: List[ServicoStatusResponse] = []


@router.post("", response_model=ClienteResponse)
def create_cliente(
    request: CreateClienteRequest,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_role(UserRole.OWNER, UserRole.EMPLOYEE)),
):
    use_case = CreateClienteUseCase(db)
    return use_case.execute(request)


@router.get("", response_model=List[ClienteResponse])
def list_clientes(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_role(UserRole.OWNER, UserRole.EMPLOYEE)),
):
    use_case = ListClientesUseCase(db)
    return use_case.execute()


@router.put("/{cliente_id}", response_model=ClienteResponse)
def update_cliente(
    cliente_id: int,
    request: UpdateClienteRequest,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_role(UserRole.OWNER, UserRole.EMPLOYEE)),
):
    use_case = UpdateClienteUseCase(db)
    return use_case.execute(cliente_id, request)


@router.delete("/{cliente_id}", status_code=204)
def delete_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_role(UserRole.OWNER, UserRole.EMPLOYEE)),
):
    use_case = DeleteClienteUseCase(db)
    use_case.execute(cliente_id)
