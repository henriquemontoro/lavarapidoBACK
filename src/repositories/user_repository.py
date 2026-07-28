from typing import Optional

from sqlalchemy.orm import Session

from src.models.user_model import UserModel


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, email: str, hashed_password: str) -> UserModel:
        user = UserModel(name=name, email=email, hashed_password=hashed_password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> Optional[UserModel]:
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[UserModel]:
        return self.db.query(UserModel).filter(UserModel.email == email).first()

    def update_password(self, user_id: int, hashed_password: str) -> Optional[UserModel]:
        user = self.get_by_id(user_id)
        if user:
            user.hashed_password = hashed_password
            self.db.commit()
            self.db.refresh(user)
        return user

    def delete(self, user_id: int) -> bool:
        user = self.get_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False
