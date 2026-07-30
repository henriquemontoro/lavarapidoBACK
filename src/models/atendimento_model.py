from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func

from src.database.database import Base


class AtendimentoModel(Base):
    __tablename__ = "atendimentos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False, index=True)
    iniciado_em = Column(DateTime, server_default=func.now(), nullable=False)
    iniciado_por_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    finalizado_em = Column(DateTime, nullable=True)
    finalizado_por_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    termo_aceito_em = Column(DateTime, nullable=True)
    termo_cpf = Column(String(20), nullable=True)
    termo_tem_plano = Column(Boolean, nullable=True)
    termo_plano = Column(String(40), nullable=True)
