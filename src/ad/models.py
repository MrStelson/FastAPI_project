from datetime import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base_model

Base = Base_model
metadata = Base.metadata


class AdType(Base):
    __tablename__ = "ad_type"
    id = Column(Integer, primary_key=True, autoincrement=True)
    type_name = Column(String, nullable=False, unique=True)
    categories = relationship(
        'AdCategory',
        back_populates='type_name'
    )


class AdCategory(Base):
    __tablename__ = "ad_category"
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String, nullable=False, unique=True)
    type_id = Column(Integer, ForeignKey('ad_type.id'))
    type_name = relationship(
        'AdType',
        back_populates='categories',
    )

    ads = relationship(
        'Ad',
        back_populates='ad_category',
        cascade='all, delete-orphan',
        passive_deletes=True
    )


class Ad(Base):
    __tablename__ = "ad"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True, default=None)
    price = Column(String, nullable=True)
    user_id = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)

    category_id = Column(Integer, ForeignKey('ad_category.id'))
    ad_category = relationship(
        'AdCategory',
        back_populates='ads'
    )

    comments = relationship(
        'AdComment',
        back_populates='ad',
    )


class AdComment(Base):
    __tablename__ = "ad_comments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    user_id = Column(Integer)

    ad_id = Column(Integer, ForeignKey('ad.id'))
    ad = relationship(
        'Ad',
        back_populates='comments',
    )
