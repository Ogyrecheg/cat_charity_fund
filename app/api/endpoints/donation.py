from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import crud_donations
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, DonationResponse
from app.services.invest_service import investment


router = APIRouter()


@router.get(
    '/',
    response_model=List[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    donations = await crud_donations.get_multi(session)
    return donations


@router.get(
    '/my',
    response_model=List[DonationResponse],
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)]
)
async def get_donations_by_user(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    donations = await crud_donations.get_by_user(session, user)
    return donations


@router.post(
    '/',
    response_model=DonationResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)],
)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    new_donation = await crud_donations.create(donation, session, user)
    await investment(session, new_donation)
    return new_donation
