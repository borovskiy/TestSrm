from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .organization_member import OrganizationMemberModel
    from .contact import ContactModel
    from .deal import DealModel
    from .activity import ActivityModel

from .base import BaseModel


class UserModel(BaseModel):
    # Модель юзеров
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))

    # Relationships
    organization_memberships: Mapped[list["OrganizationMemberModel"]] = relationship(back_populates="user")
    owned_contacts: Mapped[list["ContactModel"]] = relationship(back_populates="owner")
    user_deals: Mapped[list["DealModel"]] = relationship(back_populates="user")
    activities: Mapped[list["ActivityModel"]] = relationship(back_populates="author")