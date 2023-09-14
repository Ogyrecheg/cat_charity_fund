from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import CustomBaseModel


class Donation(CustomBaseModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
