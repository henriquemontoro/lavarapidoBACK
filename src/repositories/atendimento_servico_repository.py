from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy.orm import Session

from src.models.atendimento_servico_model import AtendimentoServicoModel


class AtendimentoServicoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_many(self, atendimento_id: int, servicos: List[str]) -> List[AtendimentoServicoModel]:
        itens = [
            AtendimentoServicoModel(atendimento_id=atendimento_id, servico=servico)
            for servico in servicos
        ]
        self.db.add_all(itens)
        self.db.commit()
        for item in itens:
            self.db.refresh(item)
        return itens

    def list_by_atendimento(self, atendimento_id: int) -> List[AtendimentoServicoModel]:
        return (
            self.db.query(AtendimentoServicoModel)
            .filter(AtendimentoServicoModel.atendimento_id == atendimento_id)
            .order_by(AtendimentoServicoModel.id)
            .all()
        )

    def get_by_id(self, item_id: int) -> Optional[AtendimentoServicoModel]:
        return self.db.query(AtendimentoServicoModel).filter(AtendimentoServicoModel.id == item_id).first()

    def set_concluido(self, item_id: int, concluido: bool, user_id: int) -> Optional[AtendimentoServicoModel]:
        item = self.get_by_id(item_id)
        if item:
            item.concluido = concluido
            item.concluido_em = datetime.now(timezone.utc) if concluido else None
            item.concluido_por_id = user_id if concluido else None
            self.db.commit()
            self.db.refresh(item)
        return item

    def all_concluidos(self, atendimento_id: int) -> bool:
        itens = self.list_by_atendimento(atendimento_id)
        return all(item.concluido for item in itens)
