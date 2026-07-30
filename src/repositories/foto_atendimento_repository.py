from typing import List, Tuple

from sqlalchemy.orm import Session

from src.models.foto_atendimento_model import FotoAtendimentoModel, MomentoFoto


class FotoAtendimentoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_many(
        self,
        atendimento_id: int,
        momento: MomentoFoto,
        registrada_por_id: int,
        arquivos: List[Tuple[bytes, str]],
    ) -> List[FotoAtendimentoModel]:
        fotos = [
            FotoAtendimentoModel(
                atendimento_id=atendimento_id,
                momento=momento,
                dados=dados,
                content_type=content_type,
                registrada_por_id=registrada_por_id,
            )
            for dados, content_type in arquivos
        ]
        self.db.add_all(fotos)
        self.db.commit()
        for foto in fotos:
            self.db.refresh(foto)
        return fotos

    def list_by_atendimento(self, atendimento_id: int, momento: MomentoFoto) -> List[FotoAtendimentoModel]:
        return (
            self.db.query(FotoAtendimentoModel)
            .filter(
                FotoAtendimentoModel.atendimento_id == atendimento_id,
                FotoAtendimentoModel.momento == momento,
            )
            .order_by(FotoAtendimentoModel.id)
            .all()
        )

    def get_by_id(self, foto_id: int):
        return self.db.query(FotoAtendimentoModel).filter(FotoAtendimentoModel.id == foto_id).first()

    def count_by_atendimento(self, atendimento_id: int) -> dict:
        fotos = (
            self.db.query(FotoAtendimentoModel)
            .filter(FotoAtendimentoModel.atendimento_id == atendimento_id)
            .all()
        )
        return {
            "inicio": sum(1 for f in fotos if f.momento == MomentoFoto.INICIO),
            "fim": sum(1 for f in fotos if f.momento == MomentoFoto.FIM),
        }
