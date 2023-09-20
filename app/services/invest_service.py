from datetime import datetime as dt
from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation


async def close_obj(
        obj: Union[CharityProject, Donation]
):
    obj.fully_invested = True
    obj.close_date = dt.utcnow()


async def get_not_invested(
        session: AsyncSession
):
    project = await session.execute(select(CharityProject).where(
        CharityProject.fully_invested == 0
    ).order_by('create_date'))
    project = project.scalars().first()
    donation = await session.execute(select(Donation).where(
        Donation.fully_invested == 0
    ).order_by('create_date'))
    donation = donation.scalars().first()

    return project, donation


async def investment(
        session: AsyncSession,
        obj: Union[CharityProject, Donation]
):
    project, donation = await get_not_invested(session)
    if not project or not donation:
        await session.commit()
        await session.refresh(obj)
        return obj
    balance_project = project.full_amount - project.invested_amount
    balance_donation = donation.full_amount - donation.invested_amount
    if balance_project > balance_donation:
        project.invested_amount += balance_donation
        donation.invested_amount = balance_donation
        await close_obj(donation)
    elif balance_project == balance_donation:
        project.invested_amount = balance_donation
        donation.invested_amount = balance_donation

        await close_obj(project)
        await close_obj(donation)
    else:
        project.invested_amount = balance_project
        donation.invested_amount = balance_project

        await close_obj(project)
    session.add(project)
    session.add(donation)
    await session.commit()
    await session.refresh(project)
    await session.refresh(donation)
    await session.refresh(obj)

    return await investment(session, obj)
