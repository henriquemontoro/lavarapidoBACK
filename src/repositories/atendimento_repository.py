from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy.orm import Session

from src.models.atendimento_model import AtendimentoModel
from src.models.atendimento_servico_model import AtendimentoServicoModel
from src.models.foto_atendimento_model import FotoAtendimentoModel


class AtendimentoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, cliente_id: int, iniciado_por_id: int) -> AtendimentoModel:
        atendimento = AtendimentoModel(cliente_id=cliente_id, iniciado_por_id=iniciado_por_id)
        self.db.add(atendimento)
        self.db.commit()
        self.db.refresh(atendimento)
        return atendimento

    def get_by_id(self, atendimento_id: int) -> Optional[AtendimentoModel]:
        return self.db.query(AtendimentoModel).filter(AtendimentoModel.id == atendimento_id).first()

    def get_ativo_by_cliente_id(self, cliente_id: int) -> Optional[AtendimentoModel]:
        return (
            self.db.query(AtendimentoModel)
            .filter(AtendimentoModel.cliente_id == cliente_id, AtendimentoModel.finalizado_em.is_(None))
            .first()
        )

    def list_ativos(self) -> List[AtendimentoModel]:
        return self.db.query(AtendimentoModel).filter(AtendimentoModel.finalizado_em.is_(None)).all()

    def list_all(self) -> List[AtendimentoModel]:
        return self.db.query(AtendimentoModel).all()

    def get_ultimo_by_cliente_id(self, cliente_id: int) -> Optional[AtendimentoModel]:
        return (
            self.db.query(AtendimentoModel)
            .filter(AtendimentoModel.cliente_id == cliente_id)
            .order_by(AtendimentoModel.id.desc())
            .first()
        )

    def aceitar_termo(
        self,
        atendimento_id: int,
        cpf: str,
        tem_plano: bool,
        plano: Optional[str],
    ) -> Optional[AtendimentoModel]:
        atendimento = self.get_by_id(atendimento_id)
        if atendimento:
            atendimento.termo_aceito_em = datetime.now(timezone.utc)
            atendimento.termo_cpf = cpf
            atendimento.termo_tem_plano = tem_plano
            atendimento.termo_plano = plano
            self.db.commit()
            self.db.refresh(atendimento)
        return atendimento

    def limpar_termo(self, atendimento_id: int) -> Optional[AtendimentoModel]:
        atendimento = self.get_by_id(atendimento_id)
        if atendimento:
            atendimento.termo_aceito_em = None
            atendimento.termo_cpf = None
            atendimento.termo_tem_plano = None
            atendimento.termo_plano = None
            self.db.commit()
            self.db.refresh(atendimento)
        return atendimento

    def list_com_termo_aceito(self) -> List[AtendimentoModel]:
        return (
            self.db.query(AtendimentoModel)
            .filter(AtendimentoModel.termo_aceito_em.isnot(None))
            .order_by(AtendimentoModel.termo_aceito_em.desc())
            .all()
        )

    def finalizar(self, atendimento_id: int, finalizado_por_id: int) -> Optional[AtendimentoModel]:
        atendimento = self.get_by_id(atendimento_id)
        if atendimento:
            atendimento.finalizado_em = datetime.now(timezone.utc)
            atendimento.finalizado_por_id = finalizado_por_id
            self.db.commit()
            self.db.refresh(atendimento)
        return atendimento

    def delete_all_by_cliente_id(self, cliente_id: int) -> None:
        atendimento_ids = [
            row.id
            for row in self.db.query(AtendimentoModel.id)
            .filter(AtendimentoModel.cliente_id == cliente_id)
            .all()
        ]
        if atendimento_ids:
            self.db.query(FotoAtendimentoModel).filter(
                FotoAtendimentoModel.atendimento_id.in_(atendimento_ids)
            ).delete(synchronize_session=False)
            self.db.query(AtendimentoServicoModel).filter(
                AtendimentoServicoModel.atendimento_id.in_(atendimento_ids)
            ).delete(synchronize_session=False)
        self.db.query(AtendimentoModel).filter(AtendimentoModel.cliente_id == cliente_id).delete()
        self.db.commit()
