from datetime import datetime

from sqlalchemy import DateTime, func, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.inspection import inspect

class BaseModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Дата создания, по умолчанию текущее время на уровне БД
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    # Дата обновления, автоматически обновляется на уровне БД при изменении записи
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    def to_dict(self) -> dict:
        mapper = inspect(self).mapper
        return {column.key: getattr(self, column.key) for column in mapper.columns}