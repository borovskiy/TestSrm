import logging
from typing import Annotated


from fastapi import APIRouter, Depends

from app.dependencies import auth_services
from app.schemas.auth_schemas import LoginUserReq, TokenFullRes, UserRegisterSchemaReq, TokenAccessRes
from app.services.auth_service import AuthService
from app.settings import settings

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/v1",
    tags=["Authentication"],
)

@router.get("/healthcheck", status_code=200)
async def healthcheck():
    """
    Привычка для для пинга авс
    """
    print(settings.DATABASE_URL)
    return {"status": "OK"}


@router.post("/register", status_code=201)
async def register(
        register_user: UserRegisterSchemaReq,
        auth_serv: Annotated[AuthService, Depends(auth_services)],
):
    """
    Регистрация пользователя
    """
    logger.info("Try get user service")
    return await auth_serv.register_user(register_user)

@router.post("/login", response_model=TokenFullRes)
async def login(
        data_user: LoginUserReq,
        auth_serv: Annotated[AuthService, Depends(auth_services)],
):
    """
    Логинимся и получаем токены
    """
    logger.info("Try get user service")
    return await auth_serv.login_user(data_user.email, data_user.password)


@router.post("/refresh_token", response_model=TokenAccessRes)
async def refresh_token(
        refresh_token_user: str,
        auth_serv: Annotated[AuthService, Depends(auth_services)],
):
    """
    Получаешь новый токен по рефрэшу
    """
    logger.info("Try get user service")
    return auth_serv.refresh_token(refresh_token_user)
