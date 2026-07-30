from typing import List, Optional

from sqlalchemy.orm import Session

from src.models.cliente_model import ClienteModel


class ClienteRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self, nome: str, sobrenome: str, telefone: str, modelo_carro: str, placa: Optional[str] = None
    ) -> ClienteModel:
        cliente = ClienteModel(
            nome=nome,
            sobrenome=sobrenome,
            telefone=telefone,
            modelo_carro=modelo_carro,
            placa=placa,
        )
        self.db.add(cliente)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def list_all(self) -> List[ClienteModel]:
        return self.db.query(ClienteModel).order_by(ClienteModel.created_at.desc(), ClienteModel.id.desc()).all()

    def get_by_id(self, cliente_id: int) -> Optional[ClienteModel]:
        return self.db.query(ClienteModel).filter(ClienteModel.id == cliente_id).first()

    def update(
        self,
        cliente_id: int,
        nome: str,
        sobrenome: str,
        telefone: str,
        modelo_carro: str,
        placa: Optional[str] = None,
    ) -> Optional[ClienteModel]:
        cliente = self.get_by_id(cliente_id)
        if cliente:
            cliente.nome = nome
            cliente.sobrenome = sobrenome
            cliente.telefone = telefone
            cliente.modelo_carro = modelo_carro
            cliente.placa = placa
            self.db.commit()
            self.db.refresh(cliente)
        return cliente

    def delete(self, cliente_id: int) -> bool:
        cliente = self.get_by_id(cliente_id)
        if cliente:
            self.db.delete(cliente)
            self.db.commit()
            return True
        return False
