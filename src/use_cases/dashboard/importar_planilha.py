import io
from datetime import date, datetime
from typing import List

import pandas as pd
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.repositories.lavagem_repository import LavagemRepository
from src.utils.lavagem_schema import (
    COLUNAS_NUMERICAS_FLOAT,
    COLUNAS_NUMERICAS_INT,
    COLUNAS_OBRIGATORIAS,
    COLUNAS_TEXTO_LIVRE,
    FORMATO_DATA_ESPERADO,
    METODOS_PAGAMENTO_VALIDOS,
    TIPOS_CARRO_VALIDOS,
)

MAX_ERROS_RETORNADOS = 50


class ImportarPlanilhaResponse(BaseModel):
    abas_processadas: int
    linhas_lidas: int
    linhas_importadas: int
    linhas_novas: int
    linhas_atualizadas: int
    linhas_rejeitadas: int
    erros: List[str]
    total_erros: int


class ImportarPlanilhaUseCase:
    def __init__(self, db: Session):
        self.repository = LavagemRepository(db)

    def execute(self, conteudo: bytes) -> ImportarPlanilhaResponse:
        try:
            planilha = pd.ExcelFile(io.BytesIO(conteudo))
        except Exception as exc:
            raise ValueError(f"Não foi possível ler o arquivo como .xlsx: {exc}") from exc

        linhas_validas: dict = {}
        erros: List[str] = []
        linhas_lidas = 0

        for nome_aba in planilha.sheet_names:
            df = pd.read_excel(planilha, sheet_name=nome_aba, dtype=object)
            linhas_lidas += len(df)

            colunas_aba = set(df.columns)
            faltando = set(COLUNAS_OBRIGATORIAS) - colunas_aba
            extras = colunas_aba - set(COLUNAS_OBRIGATORIAS)
            if faltando or extras:
                partes = []
                if faltando:
                    partes.append(f"faltando: {', '.join(sorted(faltando))}")
                if extras:
                    partes.append(f"colunas inesperadas: {', '.join(sorted(extras))}")
                erros.append(f"Aba '{nome_aba}': {'; '.join(partes)} — aba inteira ignorada.")
                continue

            for posicao, linha in df.iterrows():
                numero_linha = posicao + 2  # linha 1 é o cabeçalho
                try:
                    registro = self._validar_linha(linha)
                except ValueError as exc:
                    erros.append(f"Aba '{nome_aba}', linha {numero_linha}: {exc}")
                    continue
                linhas_validas[registro["id_lavagem"]] = registro

        resultado = self.repository.upsert_lote(list(linhas_validas.values()))

        return ImportarPlanilhaResponse(
            abas_processadas=len(planilha.sheet_names),
            linhas_lidas=linhas_lidas,
            linhas_importadas=len(linhas_validas),
            linhas_novas=resultado["novas"],
            linhas_atualizadas=resultado["atualizadas"],
            linhas_rejeitadas=linhas_lidas - len(linhas_validas),
            erros=erros[:MAX_ERROS_RETORNADOS],
            total_erros=len(erros),
        )

    def _validar_linha(self, linha) -> dict:
        registro: dict = {}

        id_lavagem = linha.get("id_lavagem")
        if pd.isna(id_lavagem):
            raise ValueError("id_lavagem vazio")
        try:
            registro["id_lavagem"] = int(id_lavagem)
        except (TypeError, ValueError):
            raise ValueError(f"id_lavagem inválido: {id_lavagem!r}")

        registro["data"] = self._parse_data(linha.get("data"))

        for campo in ("ano", "mes"):
            valor = linha.get(campo)
            if pd.isna(valor):
                raise ValueError(f"{campo} vazio")
            try:
                registro[campo] = int(valor)
            except (TypeError, ValueError):
                raise ValueError(f"{campo} inválido: {valor!r}")

        for campo in COLUNAS_TEXTO_LIVRE:
            valor = linha.get(campo)
            if pd.isna(valor) or not str(valor).strip():
                raise ValueError(f"{campo} vazio")
            registro[campo] = str(valor).strip()

        tipo_carro = str(linha.get("tipo_carro")).strip() if not pd.isna(linha.get("tipo_carro")) else ""
        if tipo_carro not in TIPOS_CARRO_VALIDOS:
            raise ValueError(
                f"tipo_carro '{tipo_carro}' fora do padrão. Valores aceitos: "
                f"{', '.join(sorted(TIPOS_CARRO_VALIDOS))}"
            )
        registro["tipo_carro"] = tipo_carro

        metodo_pagamento_bruto = linha.get("metodo_pagamento")
        metodo_pagamento = str(metodo_pagamento_bruto).strip() if not pd.isna(metodo_pagamento_bruto) else ""
        if metodo_pagamento not in METODOS_PAGAMENTO_VALIDOS:
            raise ValueError(
                f"metodo_pagamento '{metodo_pagamento}' fora do padrão. Valores aceitos: "
                f"{', '.join(sorted(METODOS_PAGAMENTO_VALIDOS))}"
            )
        registro["metodo_pagamento"] = metodo_pagamento

        for campo in COLUNAS_NUMERICAS_FLOAT:
            valor = linha.get(campo)
            if pd.isna(valor):
                raise ValueError(f"{campo} vazio")
            try:
                registro[campo] = float(valor)
            except (TypeError, ValueError):
                raise ValueError(f"{campo} deve ser numérico (ponto decimal), recebido: {valor!r}")

        for campo in COLUNAS_NUMERICAS_INT:
            valor = linha.get(campo)
            if pd.isna(valor):
                raise ValueError(f"{campo} vazio")
            try:
                registro[campo] = int(valor)
            except (TypeError, ValueError):
                raise ValueError(f"{campo} deve ser numérico inteiro, recebido: {valor!r}")

        return registro

    @staticmethod
    def _parse_data(valor) -> date:
        if valor is None or (isinstance(valor, float) and pd.isna(valor)):
            raise ValueError("data vazia")
        if isinstance(valor, datetime):
            return valor.date()
        if isinstance(valor, date):
            return valor
        if isinstance(valor, str):
            try:
                return datetime.strptime(valor.strip(), FORMATO_DATA_ESPERADO).date()
            except ValueError:
                raise ValueError(
                    f"data '{valor}' fora do padrão exigido (AAAA-MM-DD)"
                )
        raise ValueError(f"data em formato não reconhecido: {valor!r}")
