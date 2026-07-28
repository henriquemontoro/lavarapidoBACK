from typing import List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime

from src.database.database import get_db
from src.middlewares.require_role import require_role
from src.models.user_model import UserModel, UserRole
from src.use_cases.clientes.create_cliente import CreateClienteRequest, CreateClienteUseCase
from src.use_cases.clientes.list_clientes import ListClientesUseCase

router = APIRouter(prefix="/clientes", tags=["clientes"])


class ClienteResponse(BaseModel):
    id: int
    nome: str
    sobrenome: str
    telefone: str
    modelo_carro: str
    atendimento_ativo_id: Optional[int] = None
    atendimento_iniciado_em: Optional[datetime] = None


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
