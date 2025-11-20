import logging

from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.context_user import get_current_user
from app.models import OrganizationMemberModel
from app.repositories.organization_members_repository import OrganizationMemberRepository
from app.repositories.organization_repository import OrganizationRepository
from app.schemas.organisation_schemas import OrganizationCreateSchema
from app.services.base_services import BaseServices
from app.utils.raises import _not_found

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
security_bearer = HTTPBearer(auto_error=False)

logger = logging.getLogger(__name__)


class OrganizationService(BaseServices):
    def __init__(self, session: AsyncSession):
        super().__init__()
        # self.repo_user = UserRepository(session)
        self.repo_org = OrganizationRepository(session)
        self.repo_org_mem = OrganizationMemberRepository(session)

    async def create_organization(self, register_schema: OrganizationCreateSchema) -> bool:
        self.log.info("create_organization")
        if await self.repo_org.checking_existence_organization(register_schema.name):
            raise _not_found(f"Such an organization {register_schema.name} exists")
        org = await self.repo_org.create_one_obj_model(register_schema.model_dump())
        return org

    async def update_name_organization(self, id_organization: int, register_schema: OrganizationCreateSchema) -> bool:
        self.log.info("create_organization")
        if await self.repo_org.checking_existence_organization(register_schema.name):
            raise _not_found(f"Such an organization {register_schema.name} exists")
        org = await self.repo_org.update_model_id(id_organization, register_schema.model_dump())
        return org

    async def get_list_organisations(self) -> list:
        self.log.info("create_organization")
        org = await self.repo_org.get_list_obj_for_user(user_id=get_current_user().id)
        return org

    async def get_user_organisations(self, user_id: int, ogr_id: int) -> OrganizationMemberModel | None:
        self.log.info("get_user_organisations")
        return await self.repo_org_mem.get_members_in_organisation(ogr_id, user_id)
