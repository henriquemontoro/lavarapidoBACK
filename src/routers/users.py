from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.database.database import get_db
from src.middlewares.require_role import require_role
from src.models.user_model import UserModel, UserRole
from src.use_cases.users.create_user import CreateUserRequest, CreateUserUseCase
from src.use_cases.users.delete_user import DeleteUserUseCase
from src.use_cases.users.list_users import ListUsersUseCase
from src.use_cases.users.update_user import UpdateUserRequest, UpdateUserUseCase

router = APIRouter(prefix="/users", tags=["users"])


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: UserRole
    is_active: bool


@router.get("", response_model=List[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_role(UserRole.OWNER)),
):
    use_case = ListUsersUseCase(db)
    return use_case.execute()


@router.post("", response_model=UserResponse)
def create_user(
    request: CreateUserRequest,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_role(UserRole.OWNER)),
):
    use_case = CreateUserUseCase(db)
    return use_case.execute(request)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    request: UpdateUserRequest,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_role(UserRole.OWNER)),
):
    use_case = UpdateUserUseCase(db)
    return use_case.execute(user_id, request, current_user)


@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_role(UserRole.OWNER)),
):
    use_case = DeleteUserUseCase(db)
    use_case.execute(user_id, current_user)
