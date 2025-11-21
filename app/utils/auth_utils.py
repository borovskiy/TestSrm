import os

from jwt import InvalidTokenError, ExpiredSignatureError
from passlib.context import CryptContext
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from app.schemas.auth_schemas import TokenFullRes, UserSchemaPayload
from app.settings import settings
from app.utils.raises import _unauthorized


class AuthUtils:
    pwd_context = CryptContext(
        schemes=["bcrypt"],
        deprecated="auto",
    )

    # @staticmethod
    # async def issue_email_verify_token(user_id: int, type_token: TypeTokensEnum = TypeTokensEnum.email_verify) -> str:
    #     logger.info("Issue email verify token")
    #     now = datetime.now(timezone.utc)
    #     payload = PayloadToken(
    #         token_limit_verify=int((now + timedelta(minutes=settings.VERIFY_TOKEN_TTL_MIN)).timestamp()),
    #         time_now=int(now.timestamp()),
    #         user_id=user_id,
    #         type=type_token.name)
    #
    #     return jwt.encode(payload.model_dump(), settings.JWT_SECRET, algorithm=settings.JWT_ALG)
    #
    # @staticmethod
    # async def check_active_and_confirmed_user(user: UserModel) -> bool | HTTPException:
    #     logger.info("Check active and confirmed user")
    #     return await AuthUtils.check_active_user(user) and await AuthUtils.check_confirmed_user(user)
    #
    # @staticmethod
    # async def check_active_user(user: UserModel) -> bool | HTTPException:
    #     logger.info("Check active user")
    #     if not user.is_active:
    #         logger.error("User is not active")
    #         raise _unauthorized("User is not active")
    #     return True
    #
    # @staticmethod
    # async def check_confirmed_user(user: UserModel) -> bool | HTTPException:
    #     logger.info("Check confirmed user")
    #     if not user.is_confirmed or user.is_confirmed == False:
    #         logger.error("User is not confirmed")
    #         raise _unauthorized("User is not confirmed")
    #     return True
    #
    @staticmethod
    async def hash_password(plain: str) -> str:
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(plain.encode(), salt).decode()

    @staticmethod
    async def verify_password(plain: str, hashed: str) -> bool:
        return bcrypt.checkpw(plain.encode(), hashed.encode())

    @staticmethod
    def create_access_token(data: "UserSchemaPayload"):
        expire = datetime.now(timezone.utc) + timedelta(days=settings.VERIFY_TOKEN_TTL_MIN)
        data.exp = int(expire.timestamp())
        return jwt.encode(
            data.model_dump(),
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALG
        )

    @staticmethod
    def create_refresh_token(data: "UserSchemaPayload"):
        expire = datetime.now(timezone.utc) + timedelta(days=settings.VERIFY_TOKEN_TTL_MIN)
        data.exp = int(expire.timestamp())
        return jwt.encode(
            dict(data.model_dump()),
            settings.JWT_SECRET_REFRESH,
            algorithm=settings.JWT_ALG
        )

    @staticmethod
    def create_tokens(data: UserSchemaPayload) -> TokenFullRes:
        tokens = TokenFullRes(
            access_token=AuthUtils.create_access_token(data),
            refresh_token=AuthUtils.create_refresh_token(data)
        )
        return tokens

    # --- Проверка токена ---
    @staticmethod
    def verify_token(token: str, refresh: bool = False) -> "UserSchemaPayload":
        try:
            secret = (
                settings.JWT_SECRET_REFRESH if refresh else settings.JWT_SECRET
            )

            decoded = jwt.decode(
                token,
                secret,
                algorithms=[settings.JWT_ALG]
            )
            return UserSchemaPayload(**decoded)

        except ExpiredSignatureError:
            raise RuntimeError("Token expired")
        except InvalidTokenError as e:
            raise RuntimeError(f"Invalid token: {e}")

    @staticmethod
    def refresh_access_token(refresh_token: str):
        payload = AuthUtils.verify_token(refresh_token, refresh=True)
        user_id = payload.get("sub")
        if user_id is None:
            raise _unauthorized("Invalid refresh token")
        new_access = AuthUtils.create_access_token({"sub": user_id})

        return {"access_token": new_access}

    # @staticmethod
    # async def get_bearer_token(
    #         credentials: HTTPAuthorizationCredentials = Depends(security_bearer),
    # ) -> str:
    #     logger.info("Get bearer token")
    #     if not credentials or credentials.scheme.lower() != "bearer":
    #         logger.warning("Authorization header missing or not Bearer")
    #         raise _unauthorized("Authorization header missing or not Bearer")
    #     return credentials.credentials

    # @staticmethod
    # async def refresh_token(payload: PayloadToken, user_id: int):
    #     if payload.token_limit_verify - datetime.now(timezone.utc).timestamp() < 0:
    #         return await AuthUtils.issue_email_verify_token(user_id, TypeTokensEnum.access)
    #     return jwt.encode(payload.model_dump(), settings.JWT_SECRET, algorithm=settings.JWT_ALG)
    #
    # @staticmethod
    # def verify_token(raw_token: str) -> PayloadToken:
    #     logger.info("verify token")
    #     try:
    #         payload = jwt.decode(
    #             raw_token,
    #             settings.JWT_SECRET,
    #             algorithms=[settings.JWT_ALG],
    #         )
    #     except ExpiredSignatureError:
    #         logger.error("Token expired")
    #         raise _unauthorized("Token expired")
    #     except InvalidSignatureError:
    #         logger.error("Invalid signature")
    #         raise _unauthorized("Invalid signature")
    #     except InvalidTokenError:
    #         logger.error("Invalid token")
    #         raise _unauthorized("Invalid token")
    #     payload = PayloadToken(**payload)
    #     logger.info("Payload Token")
    #     return payload
