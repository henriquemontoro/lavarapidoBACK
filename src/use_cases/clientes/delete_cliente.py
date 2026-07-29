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

        if self.atendimento_repository.get_ativo_by_cliente_id(cliente_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Não é possível excluir um cliente com atendimento em andamento",
            )

        self.atendimento_repository.delete_all_by_cliente_id(cliente_id)
        self.cliente_repository.delete(cliente_id)
