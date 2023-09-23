from datetime import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP, MetaData, ForeignKey
from src.database import Base_model

Base = Base_model
metadata = Base.metadata


class AdType(Base):
    __tablename__ = "ad_type"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)


class AdCategory(Base):
    __tablename__ = "ad_category"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)


class Ad(Base):
    __tablename__ = "ad"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True, default=None)
    type_id = Column(Integer, ForeignKey('ad_type.id'))
    category_id = Column(Integer, ForeignKey('ad_category.id'))
    price = Column(String, nullable=True)
    user_id = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, )
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)



    def __repr__(self):
        return f'{self.name}. Category: {self.category}.'
