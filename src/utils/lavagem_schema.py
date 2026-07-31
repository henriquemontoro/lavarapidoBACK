# Contrato de padronização da planilha de lavagens (ver etapa de tratamento
# de dados do case). Um upload só é aceito se bater exatamente com isto —
# essa lista também alimenta o texto de ajuda mostrado no front na hora do
# import, então qualquer mudança aqui precisa ser refletida lá também.

COLUNAS_OBRIGATORIAS = [
    "id_lavagem",
    "data",
    "ano",
    "mes",
    "dia_semana",
    "cliente",
    "cpf",
    "tipo_carro",
    "funcionario_lavagem",
    "t_teto_vidros_min",
    "t_capo_parabrisa_min",
    "t_laterais_portas_min",
    "t_traseira_min",
    "t_rodas_pneus_min",
    "t_interior_min",
    "tempo_lavagem_total_min",
    "tempo_espera_antes_lavagem_min",
    "tempo_pos_lavagem_ate_retirada_min",
    "tempo_ate_pagamento_min",
    "atendente_pagamento",
    "cnpj_receita",
    "metodo_pagamento",
    "preco_reais",
    "nps_cliente",
    "nota_google",
    "shampoo_ml",
    "cera_ml",
    "pretinho_ml",
    "aromatizante_ml",
]

TIPOS_CARRO_VALIDOS = {"Hatch", "Picape", "Sedã", "SUV", "Utilitário"}

METODOS_PAGAMENTO_VALIDOS = {
    "Cartão de crédito",
    "Cartão de débito",
    "Dinheiro",
    "Pix",
    "Fiado/Mensal",
}

COLUNAS_NUMERICAS_FLOAT = [
    "t_teto_vidros_min",
    "t_capo_parabrisa_min",
    "t_laterais_portas_min",
    "t_traseira_min",
    "t_rodas_pneus_min",
    "t_interior_min",
    "tempo_lavagem_total_min",
    "nota_google",
    "preco_reais",
]

COLUNAS_NUMERICAS_INT = [
    "tempo_espera_antes_lavagem_min",
    "tempo_pos_lavagem_ate_retirada_min",
    "tempo_ate_pagamento_min",
    "nps_cliente",
    "shampoo_ml",
    "cera_ml",
    "pretinho_ml",
    "aromatizante_ml",
]

COLUNAS_TEXTO_LIVRE = [
    "dia_semana",
    "cliente",
    "cpf",
    "funcionario_lavagem",
    "atendente_pagamento",
    "cnpj_receita",
]

FORMATO_DATA_ESPERADO = "%Y-%m-%d"
