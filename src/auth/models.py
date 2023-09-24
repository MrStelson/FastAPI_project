from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base_model

Base = Base_model
metadata = Base.metadata


class Role(Base):
    __tablename__ = "app_role"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    users = relationship(
        'User',
        back_populates='role',
    )


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "app_user"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    role_id = Column(Integer, ForeignKey("app_role.id"))
    role = relationship(
        'Role',
        back_populates='users'
    )
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
    is_banned: bool = Column(Boolean, default=False, nullable=False)
