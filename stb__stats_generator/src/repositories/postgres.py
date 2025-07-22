from typing import Protocol
from typing import Self
from typing import Sequence

from pydantic import PositiveInt
from sqlalchemy import select
from sqlalchemy import delete
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from stbcore.models.user import UserStats
from stbcore.models.message import MessageStats
from stbcore.infra.postgres import Postgres


__all__ = (
	"PostgresRepository",
	"PostgresRepositoryProtocol",
)


class PostgresRepositoryProtocol(Protocol):
	"""
	"""

	async def read_hourly_message_stats(
			self: Self,
			session: AsyncSession,
			user_tg_id: PositiveInt,
			hourly_stats_date: str
	) -> Sequence[MessageStats]:	...

	async def create_hourly_user_stats(self: Self, user_tg_id: PositiveInt) -> UserStats:	...

	async def read_hourly_user_stats(
			self: Self,
			user_tg_id: PositiveInt,
			hourly_stats_date: str,
	) -> UserStats | None:	...

	async def update_user_stats_filename(self: Self, user_stats_id: PositiveInt, filename: str) -> None:	...

	async def delete_hourly_user_stats(self: Self, user_stats_id: PositiveInt) -> None:	...


class PostgresRepositoryImpl:
	"""
	"""

	async def read_hourly_message_stats(
			self: Self,
			session: AsyncSession,
			user_tg_id: PositiveInt,
			hourly_stats_date: str
	) -> Sequence[MessageStats]:
		return (await session.execute(
			select(
				MessageStats
			).where(
				MessageStats.user_id == user_tg_id,
				MessageStats.date == hourly_stats_date,
			)
		)).scalars()

	async def create_hourly_user_stats(
			self: Self,
			user_tg_id: PositiveInt,
			hourly_stats_date: str
	) -> UserStats:
		hourly_message_stats = self.read_hourly_message_stats(
			user_tg_id=user_tg_id,
			ourly_stats_date=hourly_stats_date
		)

	async def read_hourly_user_stats(
			self: Self,
			user_tg_id: PositiveInt,
			hourly_stats_date: str,
	) -> UserStats | None:
		async with Postgres.session_maker() as session:
			return (await session.execute(
				select(
					UserStats
				).where(
					UserStats.user_id == user_tg_id,
					UserStats.date == hourly_stats_date,
				)
			)).scalar()

	async def update_user_stats_filename(self: Self, user_stats_id: PositiveInt, filename: str) -> None:
		async with Postgres.session_maker() as session:
			await session.execute(
				update(
					UserStats
				).where(
					UserStats.id == user_stats_id,
				).values({
					UserStats.report_filepath: filename,
				})
			)
			await session.commit()

	async def delete_hourly_user_stats(self: Self, user_stats_id: PositiveInt) -> None:
		async with Postgres.session_maker() as session:
			await session.execute(
				delete(
					UserStats
				).where(
					UserStats.id == user_stats_id,
				)
			)
			await session.commit()


PostgresRepository = PostgresRepositoryImpl()