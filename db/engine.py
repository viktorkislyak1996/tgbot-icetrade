from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine as create_engine
from sqlalchemy.orm import sessionmaker


def create_async_engine(url: URL | str) -> AsyncEngine:
    # проверка 1
    return create_engine(url=url, pool_pre_ping=True)


def get_session_maker(engine) -> sessionmaker:
    return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
