from sqlalchemy import String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .deal import DealModel
    from .user import UserModel

from .base import BaseModel


class ActivityModel(BaseModel):
    __tablename__ = "activities"

    deal_id: Mapped[int] = mapped_column(ForeignKey("deals.id", ondelete="CASCADE"))
    author_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    type: Mapped[str] = mapped_column(String(50))  # comment, status_changed, task_created, system
    payload: Mapped[dict] = mapped_column(JSON, nullable=True)

    # Relationships
    deal: Mapped["DealModel"] = relationship(back_populates="activities")
    author: Mapped[Optional["UserModel"]] = relationship(back_populates="activities")