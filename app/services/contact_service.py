from math import ceil

from sqlalchemy.ext.asyncio import AsyncSession

from app.context_user import get_current_user
from app.models import ContactModel
from app.models.organization_member import RoleEnum
from app.repositories.contact_repository import ContactRepository
from app.repositories.organization_members_repository import OrganizationMemberRepository
from app.schemas.auth_schemas import UserSchemaPayload
from app.schemas.contact_schema import ContactsAddSchema
from app.schemas.paginate_schema import PaginationGet, ContactsPage, PageMeta
from app.services.base_services import BaseServices
from app.utils.raises import _forbidden, _not_found


class ContactService(BaseServices):
    def __init__(self, session: AsyncSession):
        super().__init__()
        self.cont_org_rep = ContactRepository(session)
        self.org_mem_rep = OrganizationMemberRepository(session)

        self.valid_roles = [
            RoleEnum.OWNER.value,
            RoleEnum.MANAGER.value,
            RoleEnum.ADMIN.value,
        ]

    async def get_contacts(self, pag: PaginationGet):
        current_user = get_current_user()
        contacts, total = await self.cont_org_rep.get_contacts_organisation(current_user.organization_id, pag)
        pages = ceil(total / pag.page_size) if pag.page_size else 1

        return ContactsPage(
            meta=PageMeta(total=total, limit=pag.page_size, pages=pages),
            contacts=contacts,
        )

    async def add_contacts(self, user_id: int | None, data: ContactsAddSchema) -> ContactModel:
        current_user: UserSchemaPayload = get_current_user()
        current_org_id: int = current_user.organization_id
        target_user_id = user_id or current_user.id

        if target_user_id != current_user.id and current_user.role_in_organization in self.valid_roles:
            raise _forbidden("You do not have the right to change contact data for the current user")

        if await self.org_mem_rep.get_members_in_organisation(organization_id=current_org_id,
                                                              user_id=target_user_id) is None:
            raise _forbidden("You do not have the right to change contact data for the current user")

        result = await self.cont_org_rep.add_contacts(current_org_id, target_user_id, data.model_dump())
        await self.cont_org_rep.session.commit()
        return result

    async def update_contacts(self, id_contact: int, data: ContactsAddSchema) -> ContactModel:
        current_user: UserSchemaPayload = get_current_user()
        current_org_id: int = current_user.organization_id
        contact_data: ContactModel = await self.cont_org_rep.get_contact_by_org(current_org_id, id_contact)
        if contact_data is None:
            raise _not_found("Not found contact in organisation")
        if contact_data.owner_id != current_user.id:
            if current_user.role_in_organization not in self.valid_roles:
                raise _forbidden("You do not have the right to change contact data for the current user")
        result = await self.cont_org_rep.update_model_id(id_contact, data.model_dump())
        return result
