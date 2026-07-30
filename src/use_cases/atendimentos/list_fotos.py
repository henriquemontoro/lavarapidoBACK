from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.models.foto_atendimento_model import MomentoFoto
from src.repositories.foto_atendimento_repository import FotoAtendimentoRepository
from src.repositories.user_repository import UserRepository


class ListFotosUseCase:
    def __init__(self, db: Session):
        self.foto_repository = FotoAtendimentoRepository(db)
        self.user_repository = UserRepository(db)

    def execute(self, atendimento_id: int, momento: MomentoFoto):
        fotos = self.foto_repository.list_by_atendimento(atendimento_id, momento)

        resultado = []
        for foto in fotos:
            usuario = self.user_repository.get_by_id(foto.registrada_por_id)
            resultado.append(
                {
                    "id": foto.id,
                    "registrada_em": foto.registrada_em,
                    "registrada_por": usuario.name if usuario else None,
                }
            )
        return resultado


class GetFotoUseCase:
    def __init__(self, db: Session):
        self.foto_repository = FotoAtendimentoRepository(db)

    def execute(self, foto_id: int):
        foto = self.foto_repository.get_by_id(foto_id)
        if not foto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Foto não encontrada")
        return foto
