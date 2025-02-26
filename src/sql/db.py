from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    create_async_engine,
    async_sessionmaker,
)

from src import config


class Base(AsyncAttrs, DeclarativeBase):
    pass


engine = None
session = None


async def initialize():
    global engine, session
    if engine is not None:
        raise RuntimeError("Engine already initialize!")

    engine = create_async_engine(config.env["POSTGRESQL_URI"])
    if session is not None:
        raise RuntimeError("Session already initialized!")
    session = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as conn:
        # TODO: remove dropping
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()


async def terminate():
    global engine
    if engine is None:
        raise RuntimeError("Engine not initialized!")
    await engine.dispose()


async def get_engine():
    global engine
    if engine is None:
        raise RuntimeError("Engine not initialized!")
    return engine


async def get_session():
    global session
    if session is None:
        raise RuntimeError("Session not initialized!")
    return session
