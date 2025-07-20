from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from src import config
from src.models.base import Base


class Postgres:
	engine = None
	session_maker = None

	@classmethod
	async def initialize(cls):
		if cls.engine is not None:
			raise RuntimeError("Engine already initialize!")

		cls.engine = create_async_engine(config.env["POSTGRESQL_URI"])
		cls.session_maker = async_sessionmaker(
			cls.engine,
			expire_on_commit=False,
		)

		async with cls.engine.begin() as conn:
			await conn.run_sync(Base.metadata.create_all)

	@classmethod
	async def terminate(cls) -> None:
		if cls.engine is None:
			return
		await cls.engine.dispose()