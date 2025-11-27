from datetime import datetime, timezone

from pydantic import create_model, field_validator

from app.schemas.base_schema import BaseModelSchema


class TaskCreateRouteSchema(BaseModelSchema):
    title: str
    description: str
    due_date: datetime

    @field_validator("due_date")
    def due_date_cannot_be_in_past(cls, v: datetime):
        # Если aware → преобразовать в naive UTC
        if v.tzinfo is not None:
            v = v.astimezone(timezone.utc).replace(tzinfo=None)

        now = datetime.utcnow()

        if v < now:
            raise ValueError("due_date cannot be in the past")

        return v

TaskCreateRouteFullSchema = create_model(
    "PaginationTasksWithDueGet",
    deal_id=(int | None, None),
    is_done=(bool, False),
    __base__=TaskCreateRouteSchema,
)


class TaskFullSchema(TaskCreateRouteFullSchema):
    id: int
