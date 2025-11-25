import logging
from abc import ABC

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update

from app.utils.raises import _bad_request


class BaseRepo(ABC):
    def __init__(self, session: AsyncSession):
        self.log = logging.LoggerAdapter(
            logging.getLogger(__name__),
            {"component": self.__class__.__name__}
        )
        self.session = session
        self.main_model = None

    async def create_one_obj_model(self, data: dict):
        self.log.info(f"create_one_obj_model")
        model_fields = self.main_model.__table__.columns.keys()
        filtered_data = {k: v for k, v in data.items() if k in model_fields}
        obj = self.main_model(**filtered_data)
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def get_one_obj_model(self, id_model: int):
        self.log.info("get_one_obj_model id %s", id_model)
        stmt_exercise = select(self.main_model).where(self.main_model.id == id_model)
        res = await self.session.execute(stmt_exercise)
        return res.scalars().first()

    async def update_model_id(self, id_model: int, data: dict):
        model_fields = self.main_model.__table__.columns.keys()
        filtered_data = {k: v for k, v in data.items() if k in model_fields}
        stmt = (
            update(self.main_model)
            .where(self.main_model.id == id_model)
            .values(**filtered_data)
            .execution_options(synchronize_session="fetch")
        )
        await self.session.execute(stmt)
        await self.session.commit()

        # Достаём обновлённый объект
        query = select(self.main_model).where(self.main_model.id == id_model)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_list_obj(self):
        self.log.info("get_list_obj")
        stmt_exercise = select(self.main_model)
        res = await self.session.execute(stmt_exercise)
        return res.scalars().all()

    async def execute_session_get_all(self, stmt):
        try:
            self.log.info("execute_session_get_all")
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception as ex:
            self.log.error("error execute stmt %s", stmt)
            self.log.error("Exception %s", ex)
            raise _bad_request("Unexpected error")

    async def execute_session_get_one(self, stmt):
        try:
            self.log.info("execute_session_get_one")
            result = await self.session.execute(stmt)
            return result.scalars().one_or_none()
        except Exception as ex:
            self.log.error("error execute stmt %s", stmt)
            self.log.error("Exception %s", ex)
            raise _bad_request("Unexpected error")

    async def delete_by_id(self, obj_id: int) -> bool:
        # Получаем объект
        stmt = select(self.main_model).where(self.main_model.id == obj_id)
        result = await self.session.execute(stmt)
        obj = result.scalar_one_or_none()
        # Удаляем
        await self.session.delete(obj)
        await self.session.flush()

        return True

    async def execute_session_and_commit(self, stmt):
        try:
            self.log.info("execute_session_and_commit")
            await self.session.execute(stmt)
            await self.session.commit()
        except Exception as ex:
            self.log.error("error execute stmt %s", stmt)
            self.log.error("Exception %s", ex)
            raise _bad_request("Unexpected error")
