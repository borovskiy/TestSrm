from sqlalchemy import String, ForeignKey, UniqueConstraint, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from enum import Enum as PyEnum

if TYPE_CHECKING:
    from .organization import OrganizationModel
    from .user import UserModel

from .base import BaseModel


class RoleEnum(PyEnum):
    OWNER = "owner"
    ADMIN = "admin"
    MANAGER = "manager"
    MEMBER = "member"


class OrganizationMemberModel(BaseModel):
    __tablename__ = "organization_members"

    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), nullable=False)

    # Relationships
    organization: Mapped["OrganizationModel"] = relationship(back_populates="members")
    user: Mapped["UserModel"] = relationship(back_populates="organization_memberships")

    __table_args__ = (
        UniqueConstraint('organization_id', 'user_id', name='uq_organization_user'),
    )
