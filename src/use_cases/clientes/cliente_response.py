from typing import List, Optional

from src.data.servicos_catalogo import calcular_preco_total
from src.models.atendimento_model import AtendimentoModel
from src.models.atendimento_servico_model import AtendimentoServicoModel
from src.models.cliente_model import ClienteModel


def build_cliente_response(
    cliente: ClienteModel,
    ultimo_atendimento: Optional[AtendimentoModel],
    foto_counts: Optional[dict] = None,
    servicos_status: Optional[List[AtendimentoServicoModel]] = None,
) -> dict:
    if ultimo_atendimento is None:
        status = "aguardando"
    elif ultimo_atendimento.finalizado_em is None:
        status = "em_andamento"
    else:
        status = "finalizado"

    counts = foto_counts or {"inicio": 0, "fim": 0}
    itens_servico = servicos_status or []

    return {
        "id": cliente.id,
        "nome": cliente.nome,
        "sobrenome": cliente.sobrenome,
        "telefone": cliente.telefone,
        "modelo_carro": cliente.modelo_carro,
        "placa": cliente.placa,
        "cor_carro": cliente.cor_carro,
        "servicos": cliente.servicos or [],
        "preco_total": calcular_preco_total(cliente.servicos),
        "status": status,
        "atendimento_ativo_id": ultimo_atendimento.id if status == "em_andamento" else None,
        "atendimento_iniciado_em": ultimo_atendimento.iniciado_em if ultimo_atendimento else None,
        "atendimento_finalizado_em": ultimo_atendimento.finalizado_em if ultimo_atendimento else None,
        "termo_aceito": bool(ultimo_atendimento and ultimo_atendimento.termo_aceito_em is not None),
        "ultimo_atendimento_id": ultimo_atendimento.id if ultimo_atendimento else None,
        "fotos_inicio_count": counts["inicio"],
        "fotos_fim_count": counts["fim"],
        "servicos_status": [
            {
                "id": item.id,
                "servico": item.servico,
                "concluido": item.concluido,
                "concluido_em": item.concluido_em,
            }
            for item in itens_servico
        ],
    }
