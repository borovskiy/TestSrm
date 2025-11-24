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

    async def get_contact(self, pag: PaginationGet):
        current_user = get_current_user()
        contacts, total = await self.cont_org_rep.get_contacts_organisation(current_user.org_id, pag)
        pages = ceil(total / pag.page_size) if pag.page_size else 1

        return ContactsPage(
            meta=PageMeta(total=total, limit=pag.page_size, pages=pages),
            contacts=contacts,
        )

    async def add_contact(self, user_id: int | None, data: ContactsAddSchema) -> ContactModel:
        current_user: UserSchemaPayload = get_current_user()
        current_org_id: int = current_user.org_id
        target_user_id = user_id or current_user.id

        if target_user_id != current_user.id and current_user.role_in_organization in self.valid_roles:
            raise _forbidden("You do not have the right to change contact data for the current user")

        if await self.org_mem_rep.get_member_in_organisation(org_id=current_org_id,
                                                             user_id=target_user_id) is None:
            raise _forbidden("You do not have the right to change contact data for the current user")

        result = await self.cont_org_rep.add_contacts(current_org_id, target_user_id, data.model_dump())
        await self.cont_org_rep.session.commit()
        return result

    async def update_contact(self, id_contact: int, data: ContactsAddSchema) -> ContactModel:
        current_user: UserSchemaPayload = get_current_user()
        current_org_id: int = current_user.org_id
        await self.cont_org_rep.get_check_contact_for_request(
            current_org_id,
            id_contact,
            self.valid_roles
        )

        return await self.cont_org_rep.update_model_id(id_contact, data.model_dump())

    async def delete_contact(self, id_contact: int, data: ContactsAddSchema) -> ContactModel:
        current_user: UserSchemaPayload = get_current_user()
        current_org_id: int = current_user.org_id
        await self.cont_org_rep.get_check_contact_for_request(
            current_org_id,
            id_contact,
            self.valid_roles
        )

        return await self.cont_org_rep.update_model_id(id_contact, data.model_dump())