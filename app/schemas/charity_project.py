from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, validator


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[int] = Field(None, gt=0)

    class Config:
        extra = Extra.forbid


class CharityProjectUpdate(CharityProjectBase):
    pass

    @validator('name')
    def name_cant_be_none(cls, value):
        if value is None:
            raise ValueError('Имя не может быть None')
        return value


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1)
    full_amount: int = Field(gt=0)

    @validator('name', 'description')
    def none_and_empty_not_allowed(cls, value: str):
        if not value or value is None:
            raise ValueError(
                'Все поля обязательны. "" или None не допускаются.'
            )
        return value


class CharityProjectBD(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
