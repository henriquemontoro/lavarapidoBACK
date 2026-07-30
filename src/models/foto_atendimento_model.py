import enum

from sqlalchemy import Column, DateTime, ForeignKey, Integer, LargeBinary, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.sql import func

from src.database.database import Base


class MomentoFoto(str, enum.Enum):
    INICIO = "inicio"
    FIM = "fim"


class FotoAtendimentoModel(Base):
    __tablename__ = "fotos_atendimento"

    id = Column(Integer, primary_key=True, index=True)
    atendimento_id = Column(Integer, ForeignKey("atendimentos.id"), nullable=False, index=True)
    momento = Column(
        SQLEnum(MomentoFoto, name="momento_foto", values_callable=lambda cls: [e.value for e in cls]),
        nullable=False,
    )
    dados = Column(LargeBinary, nullable=False)
    content_type = Column(String(50), nullable=False)
    registrada_em = Column(DateTime, server_default=func.now(), nullable=False)
    registrada_por_id = Column(Integer, ForeignKey("users.id"), nullable=False)
