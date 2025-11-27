from datetime import datetime
from typing import Sequence

from fastapi import Query
from pydantic import Field, create_model

from app.schemas.activity_schemas import ActivityResponseSchema
from app.schemas.base_schema import BaseModelSchema
from app.schemas.contact_schema import ContactsSchema
from app.schemas.organisation_schemas import OrganizationGetListSchema
from app.schemas.task_schemas import TaskFullSchema


class PaginationGetBase(BaseModelSchema):
    page: int = Field(default=0, ge=0)
    page_size: int = Field(default=10, ge=1)


class PaginationTasksGet(PaginationGetBase):
    deal_id: int
    only_open: bool = True


PaginationTasksWithDueGet = create_model(
    "PaginationTasksWithDueGet",
    due_before=(datetime | None, None),
    due_after=(datetime | None, None),
    __base__=PaginationTasksGet,
)


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


class TasksPage(BasePage):
    contacts: Sequence[TaskFullSchema]


class OrganisationPage(BasePage):
    organisations: Sequence[OrganizationGetListSchema]


class ActivitiesPage(BasePage):
    activities: Sequence[ActivityResponseSchema]
