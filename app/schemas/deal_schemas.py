from enum import Enum
from typing import Optional, List, Annotated, Sequence

from fastapi import Query, HTTPException
from pydantic import create_model, Field, model_validator

from app.context_user import get_current_user
from app.models.deal import DealStatus, DealStage
from app.models.organization_member import RoleEnum
from app.schemas.base_schema import BaseModelSchema
from app.utils.raises import _forbidden


class OrderEnum(str, Enum):
    asc = "asc"
    desc = "desc"


class DealOrderByEnum(str, Enum):
    created_at = "created_at"
    amount = "amount"
    title = "title"


class DealStatusByEnum(str, Enum):
    created_at = "created_at"
    amount = "amount"
    title = "title"


class DealFilterSchema(BaseModelSchema):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=200)
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    user_id: Optional[int] = None
    order_by: DealOrderByEnum = DealOrderByEnum.created_at
    order: OrderEnum = OrderEnum.desc
    @model_validator(mode="after")
    def validate_user_id_access(self):
        current_user = get_current_user()
        # Общая проверка чтобы простой участник не мог ввести параметр поиска по юзеру
        if self.user_id and self.user_id != current_user.id:
            if current_user.role_in_organization == RoleEnum.MEMBER:
                raise _forbidden("You do not have access to the filter for this user")

        return self

class CurrencyEnum(str, Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    RUB = "RUB"


class DealCreateSchema(BaseModelSchema):
    user_id: int
    title: str
    amount: float
    currency: CurrencyEnum


DealCreateSchemaFull = create_model(
    "DealCreateSchemaFull",
    organization_id=(int | None, None),
    __base__=DealCreateSchema,
)


class DealGetSchema(BaseModelSchema):
    id: int
    user_id: int
    title: str
    amount: float
    currency: CurrencyEnum
    status: DealStatus
    stage: DealStage


class DealPatchSchema(BaseModelSchema):
    status: DealStatus
    stage: DealStage


class DealListResponseSchema(BaseModelSchema):
    deals: Sequence[DealGetSchema]
    total: int
    pages: int
    page: int
    page_size: int
