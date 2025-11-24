import logging

from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.context_user import get_current_user
from app.models import OrganizationMemberModel, OrganizationModel
from app.repositories.organization_members_repository import OrganizationMemberRepository
from app.repositories.organization_repository import OrganizationRepository
from app.repositories.user_repository import UserRepository
from app.schemas.organisation_schemas import OrganizationCreateSchema, OrganizationAddUserSchema
from app.services.base_services import BaseServices
from app.utils.raises import _not_found, _forbidden

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
security_bearer = HTTPBearer(auto_error=False)

logger = logging.getLogger(__name__)


class OrganizationService(BaseServices):
    def __init__(self, session: AsyncSession):
        super().__init__()
        self.session = session
        self.repo_org = OrganizationRepository(self.session)
        self.repo_org_mem = OrganizationMemberRepository(self.session)
        self.user_repo = UserRepository(self.session)

    async def create_organization(self, register_schema: OrganizationCreateSchema) -> OrganizationModel:
        # Если такая огранизация существует. Выдаем ошибку. Если нет то создаем огранизацию
        self.log.info("create_organization")
        if await self.repo_org.checking_existence_organization_by_name(register_schema.name):
            raise _forbidden(f"Such an organization {register_schema.name} exists")
        org = await self.repo_org.create_one_obj_model(register_schema.model_dump())
        await self.repo_org.session.commit()
        return org

    async def add_member_in_organisation(self, data: OrganizationAddUserSchema) -> OrganizationModel:
        # Добавляем пользователя в организацию
        curr_user = get_current_user()
        self.log.info("add_member_in_organisation")
        user = await self.user_repo.find_user_id(data.user_id)
        await self.repo_org_mem.add_members_in_organisation(org_id=curr_user.org_id, user_id=user.id, role=data.role)
        member_org = await self.repo_org_mem.create_one_obj_model(data.model_dump())
        await self.repo_org.session.commit()
        return member_org

    async def update_name_organization(self, register_schema: OrganizationCreateSchema) -> bool:
        self.log.info("create_organization")
        if await self.repo_org.checking_existence_organization_by_id(get_current_user().org_id) is None:
            raise _not_found(f"Such an organization {register_schema.name} exists")
        org = await self.repo_org.update_model_id(get_current_user().org_id, register_schema.model_dump())
        return org

    async def get_list_organisations(self) -> list:
        self.log.info("create_organization")
        org = await self.repo_org.get_list_organisation_for_user(user_id=get_current_user().id)
        return org

    async def get_organisations_by_name(self, name: str) -> list:
        self.log.info("create_organization")
        org = await self.repo_org.get_organisation_by_name(name)
        return org

    async def get_user_organisations(self, user_id: int, ogr_id: int) -> OrganizationMemberModel | None:
        self.log.info("get_user_organisations")
        return await self.repo_org_mem.get_member_in_organisation(ogr_id, user_id)
