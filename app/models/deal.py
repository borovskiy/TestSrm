from sqlalchemy import String, DateTime, ForeignKey, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .organization import OrganizationModel
    from .contact import ContactModel
    from .user import UserModel
    from .task import TaskModel
    from .activity import ActivityModel

from .base import BaseModel


class DealModel(BaseModel):
    __tablename__ = "deals"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"))
    contact_id: Mapped[int] = mapped_column(ForeignKey("contacts.id", ondelete="CASCADE"))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    title: Mapped[str] = mapped_column(String(255))
    amount: Mapped[float] = mapped_column(Numeric(15, 2), nullable=True)
    currency: Mapped[str] = mapped_column(String(10), default="USD")
    status: Mapped[str] = mapped_column(String(50), default="new")  # new, in_progress, won, lost
    stage: Mapped[str] = mapped_column(String(100),
                                       default="qualification")  # qualification, proposal, negotiation, closed
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    organization: Mapped["OrganizationModel"] = relationship(back_populates="deals")
    contact: Mapped["ContactModel"] = relationship(back_populates="deals")
    owner: Mapped["UserModel"] = relationship(back_populates="owned_deals")
    tasks: Mapped[list["TaskModel"]] = relationship(back_populates="deal")
    activities: Mapped[list["ActivityModel"]] = relationship(back_populates="deal")