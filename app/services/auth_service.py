import logging

from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.organization_member import RoleEnum
from app.repositories.organization_members_repository import OrganizationMemberRepository
from app.repositories.organization_repository import OrganizationRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schemas import TokenFullRes, UserRegisterSchemaReq, UserSchemaPayload, TokenAccessRes
from app.schemas.organisation_schemas import OrganizationCreateSchema
from app.schemas.user_schemas import UserPayloadToken
from app.services.base_services import BaseServices
from app.services.organisation_service import OrganizationService
from app.utils.auth_utils import AuthUtils
from app.utils.raises import _conflict, _not_found, _forbidden, _ok, _unauthorized, _create

# pwd_context = CryptContext(
#     schemes=["bcrypt"],
#     deprecated="auto",
# )
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
security_bearer = HTTPBearer(auto_error=False)

logger = logging.getLogger(__name__)


class AuthService(BaseServices):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.repo_user = UserRepository(self.session)
        self.repo_org = OrganizationRepository(self.session)
        self.repo_mem_org = OrganizationMemberRepository(self.session)

        self.org_serv = OrganizationService(self.session)

    async def register_user_with_organisation(self, register_schema: UserRegisterSchemaReq) -> str:
        # Создаем пользователя и регистрируем на него организацию если он ввел organization_name
        # он станет OWNER этой организации
        self.log.info("create_user")
        find_user = await self.repo_user.find_user_email(register_schema.email)
        if find_user is not None:
            # Нельзя создать одинакового юзера
            self.log.warning(f"User with email: {register_schema.email} register")
            raise _forbidden(f"User with email: {register_schema.email} register")
        register_schema.hashed_password = await AuthUtils.hash_password(register_schema.hashed_password)
        find_user = await self.repo_user.create_one_obj_model(register_schema.model_dump())
        # Предварительно создаем юзера
        if register_schema.organization_name is not None:
            # пытаемся создать организацию если если он ввел organization_name, если организация есть получим ошибку
            organization = await self.org_serv.create_organization(OrganizationCreateSchema(name=register_schema.organization_name))
            # После создания добавляем участника в организацию
            await self.repo_mem_org.add_members_in_organisation(org_id=organization.id, user_id=find_user.id, role=RoleEnum.OWNER)
            return _create(f"User {find_user.email} created and added in organisation {organization.name}")
        await self.session.commit()
        # если огранизации небыло просто регистрируем типА
        return _create(f"User {find_user.email} created")


    async def login_user(self, user_email: str, user_password_hash: str) -> TokenFullRes | None:
        # Простой логин юзера. В случае успеха получим токены
        self.log.info("Try login user %s ", user_email)
        user_db = await self.repo_user.find_user_email(user_email)
        if user_db is None:
            self.log.warning("User not found")
            raise _not_found("User not found")
        self.log.info("Find user email %s ", user_email)
        if not await AuthUtils.verify_password(user_password_hash, user_db.hashed_password):
            self.log.warning("Wrong password")
            raise _forbidden("Wrong password")

        return AuthUtils.create_tokens(UserSchemaPayload.model_validate(user_db))

    async def refresh_token(self, refresh_token_user: str) -> TokenAccessRes | None:
        # Обычный рефреш токен
        self.log.info("Try refresh_token")
        user_payload: UserSchemaPayload = AuthUtils.verify_token(refresh_token_user, refresh=True)
        new_token = TokenAccessRes(access_token=AuthUtils.create_access_token(user_payload))
        return new_token
