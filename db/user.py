from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String, select
from sqlalchemy.orm import relationship, sessionmaker

from .base import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now())
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now())
    products = relationship("Auction", back_populates="user")

    def __repr__(self):
        return f'<User: {self.name} {self.telegram_id}>'


async def get_user_by_telegram_id(user_telegram_id: int, session: sessionmaker) -> User:
    async with session() as session:
        async with session.begin():
            result = await session.execute(select(User).where(User.telegram_id == user_telegram_id))
            user = result.scalar()
            return user


async def get_user_by_id(user_id: int, session: sessionmaker) -> User:
    async with session() as session:
        async with session.begin():
            result = await session.execute(select(User).where(User.id == user_id))
            user = result.scalar()
            return user


async def get_all_users(session: sessionmaker) -> User:
    async with session() as session:
        async with session.begin():
            result = await session.execute(select(User))
            users = result.scalars().all()
            return users


async def create_user(user_data: dict, session: sessionmaker) -> User:
    async with session() as session:
        async with session.begin():
            user = User(**user_data)
            session.add(user)
        await session.commit()
        return user
