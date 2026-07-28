from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.database import get_db
from src.middlewares.validate_user_auth_token import get_current_user
from src.models.user_model import UserModel
from src.use_cases.user.auth.login import LoginRequest, LoginUseCase
from src.use_cases.user.auth.register import RegisterRequest, RegisterUseCase
from src.use_cases.user.auth.reset import ResetPasswordRequest, ResetPasswordUseCase

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    use_case = RegisterUseCase(db)
    return use_case.execute(request)


@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    use_case = LoginUseCase(db)
    return use_case.execute(request)


@router.post("/reset")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    use_case = ResetPasswordUseCase(db)
    return use_case.execute(request)


@router.get("/me")
def get_me(current_user: UserModel = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role.value,
    }
