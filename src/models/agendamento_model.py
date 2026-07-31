from sqlalchemy import JSON, Column, DateTime, Float, Integer, String
from sqlalchemy.sql import func

from src.database.database import Base


class AgendamentoModel(Base):
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    sobrenome = Column(String(255), nullable=False)
    telefone = Column(String(30), nullable=False)
    modelo_carro = Column(String(255), nullable=False)
    placa = Column(String(10), nullable=True)
    servicos = Column(JSON, nullable=False)
    preco_total = Column(Float, nullable=False)
    data = Column(String(10), nullable=False, index=True)
    horario_inicio = Column(String(5), nullable=False)
    horario_fim = Column(String(5), nullable=False)
    status = Column(String(20), nullable=False, default="confirmado", server_default="confirmado")
    criado_em = Column(DateTime, server_default=func.now())
