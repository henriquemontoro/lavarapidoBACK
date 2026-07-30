from typing import List, Literal

from fastapi import HTTPException, status
from openai import OpenAI
from pydantic import BaseModel

from src.config.config import get_settings
from src.data.pop_documento import get_pop_documento

settings = get_settings()

SYSTEM_PROMPT = """Você é o assistente virtual do Lava-Rápido Nogueira, integrado ao Portal Nogueira.
Seu papel é ajudar o proprietário e os funcionários a entenderem e aplicarem o novo \
Procedimento Operacional Padrão (POP) da unidade, e a tirar dúvidas sobre a operação: \
papéis e responsabilidades, ordem de execução dos serviços, preços do catálogo, \
planos de assinatura, e o que fazer em cada situação de anomalia prevista no documento.

Responda sempre em português, de forma direta e prática, como quem já conhece a operação \
de cor. Baseie suas respostas exclusivamente no conteúdo do POP abaixo. Se a pergunta não \
puder ser respondida com base nesse documento, diga claramente que essa informação não \
consta no procedimento, em vez de inventar uma resposta.

--- INÍCIO DO POP ---
{pop}
--- FIM DO POP ---
"""


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatAssistenteUseCase:
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            self.client = None
        else:
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def execute(self, mensagens: List[ChatMessage]) -> str:
        if not mensagens:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Nenhuma mensagem enviada")

        if self.client is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Assistente não configurado: falta a chave da OpenAI no servidor",
            )

        system_message = {"role": "system", "content": SYSTEM_PROMPT.format(pop=get_pop_documento())}
        historico = [{"role": mensagem.role, "content": mensagem.content} for mensagem in mensagens]

        try:
            resposta = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[system_message, *historico],
                temperature=0.2,
            )
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Não foi possível obter resposta do assistente no momento",
            ) from error

        return resposta.choices[0].message.content or ""
