from math import ceil

from sqlalchemy.ext.asyncio import AsyncSession

from app.context_user import get_current_user
from app.models import ContactModel
from app.repositories.contact_repository import ContactRepository
from app.repositories.organization_members_repository import OrganizationMemberRepository
from app.schemas.contact_schema import ContactsAddSchema
from app.schemas.paginate_schema import PaginationGet, ContactsPage, PageMeta
from app.services.base_services import BaseServices


class ContactService(BaseServices):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.cont_org_rep = ContactRepository(session)
        self.org_mem_rep = OrganizationMemberRepository(session)

    async def get_contacts_org(self, pag: PaginationGet):
        current_user = get_current_user()
        contacts, total = await self.cont_org_rep.get_contacts_organisation(current_user.org_id, pag)
        pages = ceil(total / pag.page_size) if pag.page_size else 1

        return ContactsPage(
            meta=PageMeta(total=total, limit=pag.page_size, pages=pages),
            contacts=contacts,
        )

    async def add_contact(self, user_id: int | None, data: ContactsAddSchema) -> ContactModel:
        await self.access_utils.check_contact_access(user_id, self.valid_roles,  False)
        result = await self.cont_org_rep.add_contacts(get_current_user().org_id, user_id, data.model_dump())
        await self.cont_org_rep.session.commit()
        return result

    async def update_contact(self, user_id: int, data: ContactsAddSchema) -> ContactModel:
        await self.access_utils.check_contact_access(user_id, self.valid_roles, True)
        result = await self.cont_org_rep.update_contact(get_current_user().org_id, user_id, data.model_dump())
        await self.session.commit()
        return result