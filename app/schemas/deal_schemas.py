from enum import Enum

from pydantic import create_model

from app.models.deal import DealStatus, DealStage
from app.schemas.base_schema import BaseModelSchema


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
