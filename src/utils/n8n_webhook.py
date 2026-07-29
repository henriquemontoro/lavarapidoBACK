import json
import logging
import urllib.request

from src.config.config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()


def _chamar_webhook(nome_evento: str, webhook_url: str, telefone: str, modelo_carro: str) -> None:
    """Dispara um webhook do n8n. Nunca levanta exceção: uma falha aqui não
    pode impedir a operação (iniciar/finalizar atendimento) de seguir."""
    if not webhook_url:
        logger.warning("Webhook %s não configurado; aviso não enviado", nome_evento)
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
            logger.info("Webhook %s disparado, status %s", nome_evento, response.status)
    except Exception:
        logger.exception("Falha ao chamar o webhook %s do n8n", nome_evento)


def notificar_inicio(telefone: str, modelo_carro: str) -> None:
    """Avisa o cliente via webhook do n8n que o atendimento começou."""
    _chamar_webhook("avisar-inicio", settings.N8N_AVISAR_INICIO_WEBHOOK_URL, telefone, modelo_carro)


def notificar_pronto(telefone: str, modelo_carro: str) -> None:
    """Avisa o cliente via webhook do n8n que o carro está pronto."""
    _chamar_webhook("avisar-pronto", settings.N8N_AVISAR_PRONTO_WEBHOOK_URL, telefone, modelo_carro)
