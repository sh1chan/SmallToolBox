from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from stbcore.core.config import settings
from stbcore.models.base import Base


class Postgres:
	engine: AsyncEngine | None = None
	session_maker: async_sessionmaker | None = None

	@classmethod
	async def initialize(cls):
		cls.engine = create_async_engine(url=settings.postgres_url)
		cls.session_maker = async_sessionmaker(cls.engine, expire_on_commit=False)

		async with cls.engine.begin() as conn:
			await conn.run_sync(Base.metadata.create_all)

	@classmethod
	async def terminate(cls) -> None:
		if cls.engine is None:
			return
		await cls.engine.dispose()