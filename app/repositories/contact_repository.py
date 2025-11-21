from sqlalchemy import select, func, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ContactModel
from app.repositories.base_repository import BaseRepo
from app.schemas.paginate_schema import PaginationGet


class ContactRepository(BaseRepo):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.main_model = ContactModel

    async def get_contacts_organisation(self, id_organisation: int, pag: PaginationGet):
        self.log.info("get_contacts_organisation")

        filters = [self.main_model.organization_id == id_organisation]

        # Фильтр по owner_id
        if pag.owner_id:
            filters.append(self.main_model.owner_id == pag.owner_id)

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
        obj.owner_id = user_id
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def get_contact_by_org(self, id_organisation: int, id_contact) -> ContactModel:
        self.log.info(f"add_contacts")
        stmt = (
            select(self.main_model)
            .where(
                and_(
                    self.main_model.organization_id == id_organisation,
                    self.main_model.id == id_contact
                )

            ))
        res = await self.session.execute(stmt)
        return res.scalars().first()
