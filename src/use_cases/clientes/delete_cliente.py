from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.repositories.atendimento_repository import AtendimentoRepository
from src.repositories.cliente_repository import ClienteRepository


class DeleteClienteUseCase:
    def __init__(self, db: Session):
        self.cliente_repository = ClienteRepository(db)
        self.atendimento_repository = AtendimentoRepository(db)

    def execute(self, cliente_id: int):
        cliente = self.cliente_repository.get_by_id(cliente_id)
        if not cliente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado")

        # Exclui mesmo com atendimento em andamento — serve de saída pra atendimentos
        # travados (ex.: termo/serviço nunca respondido) que senão nunca poderiam ser
        # removidos, já que finalizar exige essas pendências resolvidas.
        self.atendimento_repository.delete_all_by_cliente_id(cliente_id)
        self.cliente_repository.delete(cliente_id)
