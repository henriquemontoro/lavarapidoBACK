import json
import logging
import urllib.request

from src.config.config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()


def notificar_pronto(telefone: str, modelo_carro: str) -> None:
    """Avisa o cliente via webhook do n8n que o carro está pronto.

    Nunca levanta exceção: uma falha no webhook não pode impedir o
    atendimento de ser marcado como finalizado.
    """
    webhook_url = settings.N8N_AVISAR_PRONTO_WEBHOOK_URL
    if not webhook_url:
        logger.warning("N8N_AVISAR_PRONTO_WEBHOOK_URL não configurada; aviso não enviado")
        return

    payload = json.dumps({"telefone": telefone, "modelo_carro": modelo_carro}).encode("utf-8")
    request = urllib.request.Request(
        webhook_url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            logger.info("Webhook avisar-pronto disparado, status %s", response.status)
    except Exception:
        logger.exception("Falha ao chamar o webhook avisar-pronto do n8n")
