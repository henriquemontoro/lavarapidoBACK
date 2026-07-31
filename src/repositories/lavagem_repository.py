from typing import Dict, List

from sqlalchemy.orm import Session

from src.models.lavagem_model import LavagemModel

TAMANHO_LOTE = 500


class LavagemRepository:
    def __init__(self, db: Session):
        self.db = db

    def upsert_lote(self, registros: List[dict]) -> Dict[str, int]:
        if not registros:
            return {"novas": 0, "atualizadas": 0}

        ids = [registro["id_lavagem"] for registro in registros]
        existentes: set = set()
        for inicio in range(0, len(ids), TAMANHO_LOTE):
            pedaco = ids[inicio : inicio + TAMANHO_LOTE]
            encontrados = (
                self.db.query(LavagemModel.id_lavagem)
                .filter(LavagemModel.id_lavagem.in_(pedaco))
                .all()
            )
            existentes.update(id_lavagem for (id_lavagem,) in encontrados)

        novos = [registro for registro in registros if registro["id_lavagem"] not in existentes]
        atualizados = [registro for registro in registros if registro["id_lavagem"] in existentes]

        if novos:
            for inicio in range(0, len(novos), TAMANHO_LOTE):
                self.db.bulk_insert_mappings(LavagemModel, novos[inicio : inicio + TAMANHO_LOTE])
        if atualizados:
            for inicio in range(0, len(atualizados), TAMANHO_LOTE):
                self.db.bulk_update_mappings(LavagemModel, atualizados[inicio : inicio + TAMANHO_LOTE])

        self.db.commit()
        return {"novas": len(novos), "atualizadas": len(atualizados)}

    def anos_disponiveis(self) -> List[int]:
        linhas = self.db.query(LavagemModel.ano).distinct().order_by(LavagemModel.ano.desc()).all()
        return [ano for (ano,) in linhas]

    def meses_disponiveis(self, ano: int) -> List[int]:
        linhas = (
            self.db.query(LavagemModel.mes)
            .filter(LavagemModel.ano == ano)
            .distinct()
            .order_by(LavagemModel.mes)
            .all()
        )
        return [mes for (mes,) in linhas]

    def semanas_iso_disponiveis(self, ano: int) -> List[int]:
        linhas = self.db.query(LavagemModel.data).filter(LavagemModel.ano == ano).all()
        semanas = {data.isocalendar()[1] for (data,) in linhas}
        return sorted(semanas)
