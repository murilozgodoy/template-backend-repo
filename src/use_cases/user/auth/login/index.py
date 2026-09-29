from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session

from database.database import get_db
from repositories.user_repository import UserRepository
from use_cases.user.auth.login.login_dto import LoginDTO
from use_cases.user.auth.login.login_use_case import LoginUseCase

router = APIRouter()


@router.post("/user/auth/login")
def user_login(
    user_login_dto: LoginDTO, response: Response, request: Request, db: Session = Depends(get_db)
):
    user_repository = UserRepository(db)
    login_use_case = LoginUseCase(user_repository)
    return login_use_case.execute(user_login_dto, response, request)
