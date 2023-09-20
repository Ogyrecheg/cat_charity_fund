from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        charity_project_id,
        session
    )
    if not charity_project:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден'
        )
    return charity_project


async def check_name_duplicate(
        charity_project_name: str,
        session: AsyncSession,
) -> None:
    project = await charity_project_crud.get_charity_project_by_name(
        charity_project_name,
        session
    )
    if project is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!'
        )


async def check_is_the_project_invested(
        project_id: int,
        session: AsyncSession
):
    project = await charity_project_crud.get_project_by_invested_amount(
        project_id,
        session
    )
    if project:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


async def check_is_the_project_closed(
        project_id: int,
        session: AsyncSession
):
    project = await charity_project_crud.get_project_by_fully_invested(
        project_id,
        session
    )
    if project:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!'
        )


async def check_update_full_amount_value(
        obj_in_full_amount_value,
        obj_db_value,
):
    if obj_in_full_amount_value < obj_db_value:
        raise HTTPException(
            status_code=422,
            detail='Нельзя установить требуемую сумму меньше уже вложенной'
        )
