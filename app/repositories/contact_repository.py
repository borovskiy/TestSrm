from sqlalchemy import select, func, or_, and_, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.context_user import get_current_user
from app.models import ContactModel
from app.repositories.base_repository import BaseRepo
from app.schemas.contact_schema import ContactsAddSchema
from app.schemas.paginate_schema import PaginationGetCont
from app.utils.raises import _not_found, _forbidden


class ContactRepository(BaseRepo[ContactModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ContactModel)
        self.main_model = ContactModel

    async def get_contacts_organisation(self, id_org: int, pag: PaginationGetCont):
        self.log.info("get_contacts_organisation")

        filters = [self.main_model.organization_id == id_org]

        # Фильтр по owner_id
        if pag.user_id:
            filters.append(self.main_model.user_id == pag.user_id)

        # Поиск по name / email / phone
        if pag.search:
            search_value = f"%{pag.search}%"
            filters.append(
                or_(
                    self.main_model.name.ilike(search_value),
                    self.main_model.email.ilike(search_value),
                    self.main_model.phone.ilike(search_value),
                )
            )

        # Основной запрос с пагинацией
        stmt = (
            select(self.main_model)
            .where(*filters)
            .offset(pag.page_size * pag.page)
            .limit(pag.page_size)
        )
        data = await self.session.execute(stmt)
        contacts = data.scalars().all()
        self.log.info("contacts")
        # Подсчёт с теми же фильтрами
        total_stmt = select(func.count()).where(*filters)
        data_total = await self.session.execute(total_stmt)
        total = data_total.scalars().first()
        self.log.info("total")

        return contacts, total

    async def get_count_contacts(self, id_organisation: int) -> int:
        self.log.info("get_count_contacts")
        stmt_count_exercise = select(func.count()).select_from(
            select(self.main_model).where(self.main_model.organization_id == id_organisation).subquery()
        )
        return await self.execute_session_get_one(stmt_count_exercise)

    async def add_contacts(self, id_organisation: int, user_id, data: dict) -> ContactModel:
        self.log.info(f"add_contacts")
        obj = self.main_model(**data)
        obj.organization_id = id_organisation
        obj.user_id = user_id
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def get_contact_by_org(self, org_id: int, user_id_cont) -> ContactModel:
        self.log.info(f"get_contact_by_org")
        stmt = (
            select(self.main_model)
            .where(
                and_(
                    self.main_model.organization_id == org_id,
                    self.main_model.user_id == user_id_cont
                )

            ))
        res = await self.session.execute(stmt)
        return res.scalars().first()

    async def update_contact(self, id_org: int, id_user, data: ContactsAddSchema):
        stmt = (
            update(self.main_model)
            .where(
                self.main_model.organization_id == id_org,
                self.main_model.user_id == id_user,
            )
            .values(**data.model_dump())
            .returning(self.main_model)
        )

        result = await self.session.execute(stmt)
        updated_contact = result.scalar_one_or_none()

        await self.session.flush()
        return updated_contact


    async def get_check_contact_for_request(self, id_org: int, id_user, list_valid_roles: list, update: bool = False):
        if update:
            contact = await self.get_contact_by_org(id_org, id_user)
            if contact is None:
                raise _not_found("Not found contact in organisation")
        if id_user != get_current_user().id:
            if get_current_user().role_in_organization not in list_valid_roles:
                raise _forbidden("You do not have the right to change contact data for the current user")
