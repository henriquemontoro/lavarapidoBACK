from sqlalchemy.orm import Session

from src.repositories.user_repository import UserRepository


class ListUsersUseCase:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def execute(self):
        return [
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role.value,
                "is_active": user.is_active,
            }
            for user in self.repository.list_all()
        ]
