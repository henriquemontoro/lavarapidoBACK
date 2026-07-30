from typing import Optional

from src.models.atendimento_model import AtendimentoModel
from src.models.cliente_model import ClienteModel


def build_cliente_response(
    cliente: ClienteModel,
    ultimo_atendimento: Optional[AtendimentoModel],
    foto_counts: Optional[dict] = None,
) -> dict:
    if ultimo_atendimento is None:
        status = "aguardando"
    elif ultimo_atendimento.finalizado_em is None:
        status = "em_andamento"
    else:
        status = "finalizado"

    counts = foto_counts or {"inicio": 0, "fim": 0}

    return {
        "id": cliente.id,
        "nome": cliente.nome,
        "sobrenome": cliente.sobrenome,
        "telefone": cliente.telefone,
        "modelo_carro": cliente.modelo_carro,
        "placa": cliente.placa,
        "status": status,
        "atendimento_ativo_id": ultimo_atendimento.id if status == "em_andamento" else None,
        "atendimento_iniciado_em": ultimo_atendimento.iniciado_em if status == "em_andamento" else None,
        "atendimento_finalizado_em": ultimo_atendimento.finalizado_em if status == "finalizado" else None,
        "ultimo_atendimento_id": ultimo_atendimento.id if ultimo_atendimento else None,
        "fotos_inicio_count": counts["inicio"],
        "fotos_fim_count": counts["fim"],
    }
