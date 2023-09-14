from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_exists,
                                check_is_the_project_closed,
                                check_is_the_project_invested,
                                check_name_duplicate,
                                check_update_full_amount_value)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (CharityProjectBD,
                                         CharityProjectCreate,
                                         CharityProjectUpdate)
from app.services.invest_service import investment


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
async def create_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),

):
    await check_name_duplicate(charity_project.name, session)
    response = await charity_project_crud.create(charity_project, session)
    await investment(session, response)
    return response


@router.patch(
    '/{project_id}',
    response_model=CharityProjectBD,
    response_model_exclude_none=False,
    dependencies=[Depends(current_superuser)]
)
async def update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    charity_project = await check_charity_project_exists(project_id, session)
    await check_is_the_project_closed(project_id, session)
    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount:
        await check_update_full_amount_value(
            obj_in.full_amount,
            charity_project.invested_amount
        )
    charity_project = await charity_project_crud.update(
        charity_project,
        obj_in,
        session,
    )
    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectBD,
    response_model_exclude_none=False,
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    charity_project = await check_charity_project_exists(project_id, session)
    await check_is_the_project_invested(project_id, session)
    charity_project = await charity_project_crud.remove(
        charity_project,
        session
    )
    return charity_project
