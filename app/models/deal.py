from sqlalchemy import String, DateTime, ForeignKey, Numeric, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import TYPE_CHECKING
from enum import Enum as PyEnum

from .organization_member import RoleEnum

if TYPE_CHECKING:
    from .organization import OrganizationModel
    from .contact import ContactModel
    from .user import UserModel
    from .task import TaskModel
    from .activity import ActivityModel

from .base import BaseModel


class DealStatus(PyEnum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    WON = "won"
    LOST = "lost"

    @classmethod
    def list_values(cls):
        """Возвращает список значений в порядке объявления"""
        return [member.value for member in cls]

    @classmethod
    def rollback_validation(cls, name_status: str, role_request_usr: str, current_status: str) -> bool:
        # Тут важно все кроме MEMBER могут даунгрейдить статусы
        # может только перескачить статус вперед
        values = DealStatus.list_values()

        if role_request_usr != RoleEnum.MEMBER.value:
            return True
        try:
            current_index = values.index(current_status)
            target_index = values.index(name_status)
        except ValueError:
            return False
        return target_index >= current_index


class DealStage(PyEnum):
    QUALIFICATION = "qualification"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSED = "closed"

    @classmethod
    def list_values(cls):
        """Возвращает список значений в порядке объявления"""
        return [member.value for member in cls]


class DealModel(BaseModel):
    __tablename__ = "deals"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    title: Mapped[str] = mapped_column(String(255))
    amount: Mapped[float] = mapped_column(Numeric(15, 2), nullable=True)
    currency: Mapped[str] = mapped_column(String(10), default="USD")
    status: Mapped[DealStatus] = mapped_column(Enum(DealStatus), default=DealStatus.NEW, nullable=False, )
    stage: Mapped[DealStage] = mapped_column(Enum(DealStage), default=DealStage.QUALIFICATION, nullable=False, )

    # Relationships
    organization: Mapped["OrganizationModel"] = relationship(back_populates="deals")
    contact: Mapped["ContactModel"] = relationship(back_populates="deals")
    owner: Mapped["UserModel"] = relationship(back_populates="owned_deals")
    tasks: Mapped[list["TaskModel"]] = relationship(back_populates="deal")
    activities: Mapped[list["ActivityModel"]] = relationship(back_populates="deal")
