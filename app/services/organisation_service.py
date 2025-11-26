import logging
from math import ceil

from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.context_user import get_current_user
from app.models import OrganizationMemberModel, OrganizationModel
from app.repositories.deal_repository import DealRepository
from app.repositories.organization_members_repository import OrganizationMemberRepository
from app.repositories.organization_repository import OrganizationRepository
from app.repositories.user_repository import UserRepository
from app.schemas.organisation_schemas import OrganizationCreateSchema, OrganizationAddUserSchema, \
    OrganizationRemoveUserSchema
from app.schemas.paginate_schema import OrganisationPage, PageMeta, PaginationOrgGet
from app.services.base_services import BaseServices
from app.utils.raises import _not_found, _forbidden, _ok

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
security_bearer = HTTPBearer(auto_error=False)

logger = logging.getLogger(__name__)


class OrganizationService(BaseServices):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.repo_org = OrganizationRepository(self.session)
        self.repo_org_mem = OrganizationMemberRepository(self.session)
        self.user_repo = UserRepository(self.session)
        self.deal_repo = DealRepository(self.session)

    async def create_organization(self, register_schema: OrganizationCreateSchema) -> OrganizationModel:
        # Если такая огранизация существует. Выдаем ошибку. Если нет то создаем огранизацию
        self.log.info("create_organization")
        if await self.repo_org.checking_existence_organization_by_name(register_schema.name):
            raise _forbidden(f"Such an organization {register_schema.name} exists")
        org = await self.repo_org.create_one_obj_model(register_schema.model_dump())
        return org

    async def add_member_in_organisation(self, data: OrganizationAddUserSchema) -> OrganizationModel:
        # Добавляем пользователя в организацию с указанием его роли
        self.log.info("add_member_in_organisation")
        # если юзера не будет то получим ошибку
        user = await self.user_repo.find_user_id(data.user_id)
        await self.repo_org_mem.add_members_in_organisation(org_id=get_current_user().org_id, user_id=user.id,
                                                            role=data.role)
        await self.repo_org.session.commit()
        return _ok(f"User {user.email} added in your organisation")

    async def remove_member_from_organisation(self, data: OrganizationRemoveUserSchema) -> OrganizationModel:
        # Удаляем участника организации
        ## TODO есть логика запрета удаления участника при существующих сделках которой пока нет
        self.log.info("add_member_in_organisation")
        user = await self.repo_org_mem.get_member_in_organisation(org_id=get_current_user().org_id,
                                                                  user_id=data.user_id)
        if user is None:
            raise _not_found(f"User id {data.user_id} not found in organisation")

        await self.repo_org.session.commit()
        return _ok(f"User {user.email} added in your organisation")

    async def update_name_organization(self, register_schema: OrganizationCreateSchema) -> bool:
        # Обновляем имя организации
        self.log.info("create_organization")
        if await self.repo_org.get_organisation_by_name(register_schema.name) is not None:
            # если есть организацияс таким именем не сомжет создать новую
            raise _not_found(f"Such an organization {register_schema.name} exists")
        return await self.repo_org.update_model_id(get_current_user().org_id, register_schema.model_dump())

    async def get_list_organisations(self, pag: PaginationOrgGet) -> OrganisationPage:
        # Получаем список организация в которых закреплен текущий юзер
        self.log.info("get_list_organisations")
        orgs, total = await self.repo_org.get_list_organisation_for_user(user_id=get_current_user().id, pagination=pag)
        pages = ceil(total / pag.page_size) if pag.page_size else 1

        return OrganisationPage(
            meta=PageMeta(total=total, limit=pag.page_size, pages=pages),
            organisations=orgs,
        )

    async def get_organisations_by_name(self, name: str) -> list:
        self.log.info("create_organization")
        org = await self.repo_org.get_organisation_by_name(name)
        return org

    async def get_user_organisations(self, user_id: int, ogr_id: int) -> OrganizationMemberModel | None:
        self.log.info("get_user_organisations")
        return await self.repo_org_mem.get_member_in_organisation(ogr_id, user_id)
