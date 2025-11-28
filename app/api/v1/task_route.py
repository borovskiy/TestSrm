from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.core.authentication import require_roles
from app.core.dependencies import task_services
from app.models.organization_member import RoleEnum
from app.schemas.paginate_schema import PaginationTasksGet, PaginationTasksWithDueGet, TasksPage
from app.schemas.task_schemas import TaskCreateRouteSchema, TaskFullSchema
from app.services.task_service import TaskService

router = APIRouter(
    prefix="/v1/tasks",
    tags=["Task"],
)


@router.get("/",
            response_model=TasksPage,
            status_code=200,
            dependencies=[Depends(require_roles([RoleEnum.MEMBER.value, RoleEnum.OWNER.value, RoleEnum.MANAGER.value, RoleEnum.ADMIN.value, ]))])
async def get_tasks_deal(
        task_serv: Annotated[TaskService, Depends(task_services)],
        pagination: PaginationTasksGet = Depends(PaginationTasksGet),
        due_before: datetime | None = Query(example="2025-01-01T00:00:00"),
        due_after: datetime | None = Query(example="2025-01-01T00:00:00"),
):
    # Получаем таски для сделки- момент с ремоделированием из-за отсутсвия описания через падантик модели
    pag = PaginationTasksWithDueGet(**pagination.model_dump())
    pag.due_before = due_before
    pag.due_after = due_after
    return await task_serv.get_tasks_for_deals(pag)


@router.post("/{deal_id}",
             response_model=TaskFullSchema,
             status_code=201,
             dependencies=[Depends(require_roles(
                 [RoleEnum.MEMBER.value, RoleEnum.OWNER.value, RoleEnum.MANAGER.value, RoleEnum.ADMIN.value, ]))]
             )
async def crate_task_deal(
        task_serv: Annotated[TaskService, Depends(task_services)],
        data: TaskCreateRouteSchema,
        deal_id: int
):
    return await task_serv.create_tasks(data, deal_id)
