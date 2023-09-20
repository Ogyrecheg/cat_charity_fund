from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    async def get_charity_project_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        project = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        project = project.scalars().first()
        return project

    async def get_project_by_invested_amount(
            self,
            project_id: int,
            session: AsyncSession,
    ):
        project = await session.execute(
            select(CharityProject).where(
                CharityProject.invested_amount != 0
            ).where(
                CharityProject.id == project_id
            )
        )
        project = project.scalars().first()
        return project

    async def get_project_by_fully_invested(
            self,
            project_id: int,
            session: AsyncSession,
    ):
        project = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested
            ).where(
                CharityProject.id == project_id
            )
        )
        project = project.scalars().first()
        return project


charity_project_crud = CRUDCharityProject(CharityProject)
