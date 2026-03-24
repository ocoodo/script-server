from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from settings import settings


engine = create_async_engine(settings.db_url)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


class Model(DeclarativeBase):
    pass


DbSession = Annotated[AsyncSession, Depends(get_session)]


async def init_db():
    async with engine.begin() as c:
        await c.run_sync(Model.metadata.create_all)