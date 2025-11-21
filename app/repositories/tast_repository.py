from sqlalchemy.ext.asyncio import AsyncSession

from app.models import TaskModel
from app.repositories.base_repository import BaseRepo


class TaskRepository(BaseRepo):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.main_model = TaskModel