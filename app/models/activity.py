from sqlalchemy import ForeignKey, JSON, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as PyEnum
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .deal import DealModel
    from .user import UserModel

from .base import BaseModel

class TypeActivity(PyEnum):
    COMMENT = "COMMENT"
    STATUS_CHANGED = "STATUS_CHANGED"
    TASK_CREATED = "TASK_CREATED"
    SYSTEM = "SYSTEM"

class ActivityModel(BaseModel):
    __tablename__ = "activities"

    deal_id: Mapped[int] = mapped_column(ForeignKey("deals.id", ondelete="CASCADE"))
    author_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    type: Mapped[TypeActivity] = mapped_column(Enum(TypeActivity), nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, nullable=True)


    # Relationships
    deal: Mapped["DealModel"] = relationship(back_populates="activities")
    author: Mapped[Optional["UserModel"]] = relationship(back_populates="activities")