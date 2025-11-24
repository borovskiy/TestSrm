import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.organization_member import RoleEnum
from app.utils.access_utils import AccessUtils
from app.utils.raises import _forbidden


class BaseServices:
    def __init__(self, session: AsyncSession):
        self.log = logging.LoggerAdapter(
            logging.getLogger(__name__),
            {"component": self.__class__.__name__}
        )
        self.valid_roles = [
            RoleEnum.OWNER.value,
            RoleEnum.MANAGER.value,
            RoleEnum.ADMIN.value,
        ]
        self.session = session
        self.access_utils = AccessUtils(self.session)
        # self.rabbit_service = RabbitClientStateless(settings.AMQP_URL, default_queue="orders")
