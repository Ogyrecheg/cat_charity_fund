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
