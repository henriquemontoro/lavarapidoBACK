from sqlalchemy import JSON, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from src.database.database import Base


class ClienteModel(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    sobrenome = Column(String(255), nullable=False)
    telefone = Column(String(30), nullable=False)
    modelo_carro = Column(String(255), nullable=False)
    placa = Column(String(10), nullable=True)
    cor_carro = Column(String(40), nullable=True)
    servicos = Column(JSON, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
