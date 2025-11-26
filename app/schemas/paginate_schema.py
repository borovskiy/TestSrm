from typing import Sequence

from pydantic import Field

from app.schemas.activity_schemas import ActivityResponseSchema
from app.schemas.base_schema import BaseModelSchema
from app.schemas.contact_schema import ContactsSchema
from app.schemas.organisation_schemas import OrganizationGetListSchema


class PaginationGetBase(BaseModelSchema):
    page: int = Field(default=0, ge=0)
    page_size: int = Field(default=10, ge=1)


class PaginationGetActivities(PaginationGetBase):
    ...


class PaginationOrgGet(PaginationGetBase):
    search: str | None = None


class PaginationGetCont(PaginationGetBase):
    user_id: int | None = None


class PageMeta(BaseModelSchema):
    total: int
    limit: int
    pages: int


class BasePage(BaseModelSchema):
    meta: PageMeta


class ContactsPage(BasePage):
    contacts: Sequence[ContactsSchema]


class OrganisationPage(BasePage):
    organisations: Sequence[OrganizationGetListSchema]


class ActivitiesPage(BasePage):
    activities: Sequence[ActivityResponseSchema]
