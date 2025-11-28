from typing import Literal, Optional

from pydantic import Field, field_validator

from app.schemas.base_schema import BaseModelSchema


class CommentPayload(BaseModelSchema):
    text: str = Field(..., min_length=1)


class UpdateStatusDealPayload(BaseModelSchema):
    deal_before: dict
    deal_after: dict

class CreateTaskPayload(BaseModelSchema):
    task: dict

class ActivityCreateSchema(BaseModelSchema):
    type: Literal["comment"] = "comment"
    payload: dict

    @field_validator("type")
    def convert_to_enum(cls, v):
        return v.upper()


class ActivityResponseSchema(BaseModelSchema):
    id: int
    deal_id: int
    author_id: Optional[int] = None
    type: str
    payload: dict | None = None
