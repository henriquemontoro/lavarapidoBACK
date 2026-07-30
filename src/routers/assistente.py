from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from src.middlewares.require_role import require_role
from src.models.user_model import UserModel, UserRole
from src.use_cases.assistente.chat_assistente import ChatAssistenteUseCase, ChatMessage

router = APIRouter(prefix="/assistente", tags=["assistente"])


class ChatRequest(BaseModel):
    mensagens: List[ChatMessage]


class ChatResponse(BaseModel):
    resposta: str


@router.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    current_user: UserModel = Depends(require_role(UserRole.OWNER, UserRole.EMPLOYEE)),
):
    use_case = ChatAssistenteUseCase()
    resposta = use_case.execute(request.mensagens)
    return {"resposta": resposta}
