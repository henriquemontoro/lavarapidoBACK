from typing import List, Optional

from sqlalchemy.orm import Session

from src.models.user_model import UserModel, UserRole


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        name: str,
        email: str,
        hashed_password: str,
        role: UserRole = UserRole.EMPLOYEE,
    ) -> UserModel:
        user = UserModel(name=name, email=email, hashed_password=hashed_password, role=role)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def list_all(self) -> List[UserModel]:
        return self.db.query(UserModel).order_by(UserModel.name).all()

    def update(
        self, user_id: int, name: str, email: str, role: UserRole, is_active: bool
    ) -> Optional[UserModel]:
        user = self.get_by_id(user_id)
        if user:
            user.name = name
            user.email = email
            user.role = role
            user.is_active = is_active
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
