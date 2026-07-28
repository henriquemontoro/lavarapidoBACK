from fastapi import Depends, HTTPException, status

from src.middlewares.validate_user_auth_token import get_current_user
from src.models.user_model import UserModel, UserRole


def require_role(*roles: UserRole):
    def dependency(current_user: UserModel = Depends(get_current_user)) -> UserModel:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso negado",
            )
        return current_user

    return dependency
