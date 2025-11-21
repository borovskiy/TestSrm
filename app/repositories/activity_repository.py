from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ActivityModel
from app.repositories.base_repository import BaseRepo


class ActivityRepository(BaseRepo):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.main_model = ActivityModel