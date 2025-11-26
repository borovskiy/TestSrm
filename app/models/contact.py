from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .organization import OrganizationModel
    from .user import UserModel

from .base import BaseModel


class ContactModel(BaseModel):
    __tablename__ = "contacts"
    # Чисто модель контакта юзера в организации. зачем то. Кто нахуй тысячу почт держит в наше время?
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), nullable=True)
    phone: Mapped[str] = mapped_column(String(50), nullable=True)

    # Relationships
    organization: Mapped["OrganizationModel"] = relationship(back_populates="contacts")
    owner: Mapped["UserModel"] = relationship(back_populates="owned_contacts")
