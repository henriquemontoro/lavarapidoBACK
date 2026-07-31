import hmac

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from src.config.config import get_settings

_api_key_header = APIKeyHeader(name="X-N8N-Secret", auto_error=False)


def validate_webhook_secret(secret: str = Depends(_api_key_header)) -> None:
    """Autentica chamadas do n8n (não são um usuário logado) por segredo
    compartilhado, em vez de JWT/role."""
    settings = get_settings()
    if not settings.N8N_INBOUND_SECRET or not secret or not hmac.compare_digest(secret, settings.N8N_INBOUND_SECRET):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Assinatura inválida")
