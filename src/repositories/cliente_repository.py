from typing import List, Optional

from sqlalchemy.orm import Session

from src.models.cliente_model import ClienteModel


class ClienteRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, nome: str, sobrenome: str, telefone: str, modelo_carro: str) -> ClienteModel:
        cliente = ClienteModel(
            nome=nome,
            sobrenome=sobrenome,
            telefone=telefone,
            modelo_carro=modelo_carro,
        )
        self.db.add(cliente)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def list_all(self) -> List[ClienteModel]:
        return self.db.query(ClienteModel).order_by(ClienteModel.nome).all()

    def get_by_id(self, cliente_id: int) -> Optional[ClienteModel]:
        return self.db.query(ClienteModel).filter(ClienteModel.id == cliente_id).first()
