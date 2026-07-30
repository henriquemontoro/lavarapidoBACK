from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, Response, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.database.database import get_db
from src.middlewares.require_role import require_role
from src.models.foto_atendimento_model import MomentoFoto
from src.models.user_model import UserModel, UserRole
from src.use_cases.atendimentos.finalizar_atendimento import FinalizarAtendimentoUseCase
from src.use_cases.atendimentos.iniciar_atendimento import IniciarAtendimentoUseCase
from src.use_cases.atendimentos.list_fotos import GetFotoUseCase, ListFotosUseCase
from src.use_cases.atendimentos.toggle_servico import ToggleServicoUseCase

router = APIRouter(prefix="/atendimentos", tags=["atendimentos"])


class AtendimentoResponse(BaseModel):
    id: int
    cliente_id: int
    iniciado_em: Optional[datetime] = None
    finalizado_em: Optional[datetime] = None


class FotoMetadataResponse(BaseModel):
    id: int
    registrada_em: datetime
    registrada_por: Optional[str] = None


class ToggleServicoRequest(BaseModel):
    concluido: bool


class ServicoResponse(BaseModel):
    id: int
    atendimento_id: int
    servico: str
    concluido: bool


async def _read_fotos(fotos: List[UploadFile]) -> List[tuple]:
    return [(await foto.read(), foto.content_type or "image/jpeg") for foto in fotos]


@router.post("", response_model=AtendimentoResponse)
async def iniciar_atendimento(
    cliente_id: int = Form(...),
    fotos: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_role(UserRole.OWNER, UserRole.EMPLOYEE)),
):
    arquivos = await _read_fotos(fotos)
    use_case = IniciarAtendimentoUseCase(db)
    return use_case.execute(cliente_id, arquivos, current_user)


@router.post("/{atendimento_id}/finalizar", response_model=AtendimentoResponse)
async def finalizar_atendimento(
    atendimento_id: int,
    fotos: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_role(UserRole.OWNER, UserRole.EMPLOYEE)),
):
    arquivos = await _read_fotos(fotos)
    use_case = FinalizarAtendimentoUseCase(db)
    return use_case.execute(atendimento_id, arquivos, current_user)


@router.get("/{atendimento_id}/fotos", response_model=List[FotoMetadataResponse])
def list_fotos(
    atendimento_id: int,
    momento: MomentoFoto,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_role(UserRole.OWNER, UserRole.EMPLOYEE)),
):
    use_case = ListFotosUseCase(db)
    return use_case.execute(atendimento_id, momento)


@router.patch("/{atendimento_id}/servicos/{servico_id}", response_model=ServicoResponse)
def toggle_servico(
    atendimento_id: int,
    servico_id: int,
    request: ToggleServicoRequest,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_role(UserRole.OWNER, UserRole.EMPLOYEE)),
):
    use_case = ToggleServicoUseCase(db)
    return use_case.execute(atendimento_id, servico_id, request.concluido, current_user)


foto_router = APIRouter(prefix="/fotos", tags=["atendimentos"])


@foto_router.get("/{foto_id}")
def get_foto(
    foto_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_role(UserRole.OWNER, UserRole.EMPLOYEE)),
):
    use_case = GetFotoUseCase(db)
    foto = use_case.execute(foto_id)
    return Response(content=foto.dados, media_type=foto.content_type)
