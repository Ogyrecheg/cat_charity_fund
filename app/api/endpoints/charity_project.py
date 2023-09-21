from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_charity_project_exists
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (CharityProjectBD,
                                         CharityProjectCreate,
                                         CharityProjectUpdate)
from app.services.utils import (create_charity_project, delete_charity_project,
                                update_charity_project)

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectBD],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session)
):
    charity_projects = await charity_project_crud.get_multi(session)
    return charity_projects


@router.post(
    '/',
    response_model=CharityProjectBD,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),

):
    response = await create_charity_project(charity_project, session)
    return response


@router.patch(
    '/{project_id}',
    response_model=CharityProjectBD,
    response_model_exclude_none=False,
    dependencies=[Depends(current_superuser)]
)
async def update_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    charity_project = await check_charity_project_exists(project_id, session)
    charity_project = await update_charity_project(
        project_id,
        charity_project,
        obj_in,
        session
    )
    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectBD,
    response_model_exclude_none=False,
    dependencies=[Depends(current_superuser)]
)
async def delete_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    charity_project = await check_charity_project_exists(project_id, session)
    charity_project = await delete_charity_project(
        project_id,
        charity_project,
        session
    )
    return charity_project
