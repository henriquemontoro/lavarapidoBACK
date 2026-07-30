from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String

from src.database.database import Base


class AtendimentoServicoModel(Base):
    __tablename__ = "atendimento_servicos"

    id = Column(Integer, primary_key=True, index=True)
    atendimento_id = Column(Integer, ForeignKey("atendimentos.id"), nullable=False, index=True)
    servico = Column(String(80), nullable=False)
    concluido = Column(Boolean, default=False, nullable=False)
    concluido_em = Column(DateTime, nullable=True)
    concluido_por_id = Column(Integer, ForeignKey("users.id"), nullable=True)
