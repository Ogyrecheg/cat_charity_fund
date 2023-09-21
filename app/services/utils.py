from sqlalchemy.ext.asyncio import AsyncSession

from app.services.service_validators import (check_is_the_project_closed,
                                             check_is_the_project_invested,
                                             check_name_duplicate,
                                             check_update_full_amount_value)
from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectUpdate)
from app.services.invest_service import investment


async def create_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession,
):
    await check_name_duplicate(charity_project.name, session)
    response = await charity_project_crud.create(charity_project, session)
    await investment(session, response)
    return response


async def update_charity_project(
        project_id: int,
        charity_project: CharityProject,
        obj_in: CharityProjectUpdate,
        session: AsyncSession
):
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


async def delete_charity_project(
        project_id: int,
        charity_project: CharityProject,
        session: AsyncSession
):
    await check_is_the_project_invested(project_id, session)
    charity_project = await charity_project_crud.remove(
        charity_project,
        session
    )
    return charity_project
