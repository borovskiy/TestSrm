from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import UserModel
    from .contact import ContactModel
    from .deal import DealModel

from .base import BaseModel


class OrganizationModel(BaseModel):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(255))

    # Relationships
    members: Mapped[list["OrganizationMemberModel"]] = relationship(back_populates="organization")
    contacts: Mapped[list["ContactModel"]] = relationship(back_populates="organization")
    deals: Mapped[list["DealModel"]] = relationship(back_populates="organization")