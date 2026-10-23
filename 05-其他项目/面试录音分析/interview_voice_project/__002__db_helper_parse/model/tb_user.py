from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, BigInteger, Text, DateTime, SmallInteger
from sqlalchemy.schema import Index

from __002__db_helper_parse.model.base import Base


class TbUser(Base):
    __tablename__ = 'tb_user'

    user_id = Column(String(32), primary_key=True, comment='用户ID')
    user_name = Column(String(100), nullable=False, unique=True, comment='用户名')
    password = Column(String(255), nullable=False, comment='密码')

    __table_args__ = (
        # Index for faster lookup of user_id and user_name
        Index('ind_user_id', 'user_id'),
        Index('ind_user_name', 'user_name'),
    )
