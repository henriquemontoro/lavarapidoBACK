from sqlalchemy import Column, Date, Float, Integer, String

from src.database.database import Base


class LavagemModel(Base):
    __tablename__ = "lavagens"

    # id_lavagem é a chave natural que já vem padronizada e única na planilha
    # tratada; usá-la como PK torna a reimportação idempotente (upsert direto).
    id_lavagem = Column(Integer, primary_key=True, autoincrement=False)
    data = Column(Date, nullable=False, index=True)
    ano = Column(Integer, nullable=False, index=True)
    mes = Column(Integer, nullable=False, index=True)
    dia_semana = Column(String(20), nullable=False)
    cliente = Column(String(255), nullable=False)
    cpf = Column(String(20), nullable=False)
    tipo_carro = Column(String(30), nullable=False)
    funcionario_lavagem = Column(String(255), nullable=False)
    t_teto_vidros_min = Column(Float, nullable=False)
    t_capo_parabrisa_min = Column(Float, nullable=False)
    t_laterais_portas_min = Column(Float, nullable=False)
    t_traseira_min = Column(Float, nullable=False)
    t_rodas_pneus_min = Column(Float, nullable=False)
    t_interior_min = Column(Float, nullable=False)
    tempo_lavagem_total_min = Column(Float, nullable=False)
    tempo_espera_antes_lavagem_min = Column(Integer, nullable=False)
    tempo_pos_lavagem_ate_retirada_min = Column(Integer, nullable=False)
    tempo_ate_pagamento_min = Column(Integer, nullable=False)
    atendente_pagamento = Column(String(255), nullable=False)
    cnpj_receita = Column(String(255), nullable=False)
    metodo_pagamento = Column(String(30), nullable=False)
    preco_reais = Column(Float, nullable=False)
    nps_cliente = Column(Integer, nullable=False)
    nota_google = Column(Float, nullable=False)
    shampoo_ml = Column(Integer, nullable=False)
    cera_ml = Column(Integer, nullable=False)
    pretinho_ml = Column(Integer, nullable=False)
    aromatizante_ml = Column(Integer, nullable=False)
