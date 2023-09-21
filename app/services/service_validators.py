from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.services.service_constants import (BAD_REQUEST_CODE,
                                            FULL_AMOUNT_ERROR_MSG,
                                            PROJECT_CLOSED_ERROR_MSG,
                                            PROJECT_DUPLICATE_ERROR_MSG,
                                            PROJECT_INVESTED_ERROR_MSG,
                                            UNPROCESSABLE_ENTITY)


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
            status_code=BAD_REQUEST_CODE,
            detail=PROJECT_DUPLICATE_ERROR_MSG
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
            status_code=BAD_REQUEST_CODE,
            detail=PROJECT_INVESTED_ERROR_MSG
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
            status_code=BAD_REQUEST_CODE,
            detail=PROJECT_CLOSED_ERROR_MSG
        )


async def check_update_full_amount_value(
        obj_in_full_amount_value,
        obj_db_value,
):
    if obj_in_full_amount_value < obj_db_value:
        raise HTTPException(
            status_code=UNPROCESSABLE_ENTITY,
            detail=FULL_AMOUNT_ERROR_MSG
        )
