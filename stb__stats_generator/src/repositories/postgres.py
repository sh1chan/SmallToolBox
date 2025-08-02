from typing import Protocol
from typing import Self
from typing import Sequence
from itertools import groupby
from collections import defaultdict

from pydantic import PositiveInt
from pydantic import NegativeInt
from sqlalchemy import select
from sqlalchemy import delete
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from stbcore.models.user import UserStats
from stbcore.models.chat import Chat
from stbcore.models.chat import ChatStats
from stbcore.models.message import MessageStats
from stbcore.infra.postgres import Postgres


__all__ = (
	"PostgresRepository",
	"PostgresRepositoryProtocol",
)


def parse_h_from_dt(dt: str) -> int:
	"""
	"""
	return int(dt.split(" ")[1].split(":")[0])


class MessageStatsRepositoryProtocol(Protocol):
	"""
	"""

	async def read(
			self: Self,
			user_id: PositiveInt | None,
			chat_id: NegativeInt | None,
			date: str,
			session: AsyncSession,
	) -> Sequence[MessageStats]:	...


class MessageStatsRepositoryImpl:
	"""
	"""

	async def read(
			self: Self,
			user_id: PositiveInt | None,
			chat_id: NegativeInt | None,
			date: str,
			session: AsyncSession,
	) -> Sequence[MessageStats]:
		"""
		"""
		date = date.split()[0]
		filters = [
			MessageStats.date.startswith(date)
		]
		if user_id:
			filters.append(
				MessageStats.user_id == user_id
			)
		if chat_id:
			filters.append(
				MessageStats.chat_id == chat_id
			)

		return (
			await session.execute(
				select(
					MessageStats
				).where(
					*filters
				).order_by(
					MessageStats.id
				)
			)
		).scalars().all()


class ChatRepositoryProtocol(Protocol):
	"""
	"""

	async def read(
			self: Self,
			chat_id: NegativeInt,
			session: AsyncSession,
	) -> Chat | None:	...


class ChatRepositoryImpl:
	"""
	"""

	async def read(
			self: Self,
			chat_id: NegativeInt,
			session: AsyncSession,
	) -> Chat | None:
		"""
		"""
		return await session.get(
			entity=Chat,
			ident=chat_id,
		)


class ChatStatsRepositoryProtocol(Protocol):
	"""
	"""

	async def create(
			self: Self,
			chat_id: NegativeInt,
			date: str,
			users_count: int,
			messages_count: int,
			data: defaultdict,
			filename: str,
			session: AsyncSession,
	) -> ChatStats:	...

	async def read(
			self: Self,
			chat_id: NegativeInt,
			session: AsyncSession,
	) -> ChatStats | None:	...

	async def delete(
			self: Self,
			chat_stats_id: NegativeInt,
			session: AsyncSession,
	) -> None:	...


class ChatStatsRepositoryImpl:
	"""
	"""

	async def create(
			self: Self,
			chat_id: NegativeInt,
			date: str,
			users_count: int,
			messages_count: int,
			data: defaultdict,
			filename: str,
			session: AsyncSession,
	) -> ChatStats:
		"""
		"""
		chat_stats = ChatStats(
			date=date,
			users_count=users_count,
			messages_count=messages_count,
			data=data,
			report_filepath=filename,
			chat_id=chat_id,
		)
		session.add(chat_stats)
		await session.commit()

		return chat_stats

	async def read(
			self: Self,
			chat_id: NegativeInt,
			date: str,
			session: AsyncSession,
	) -> ChatStats | None:
		"""
		"""
		return await session.scalar(
			select(
				ChatStats
			).where(
				chat_id=chat_id,
				date=date,
			)
		)

	async def delete(
			self: Self,
			chat_stats_id: NegativeInt,
			session: AsyncSession,
	) -> None:
		"""
		"""
		await session.execute(
			delete(
				ChatStats
			).where(
				ChatStats.id == chat_stats_id,
			)
		)


class UserStatsRepositoryProtocol(Protocol):
	"""
	"""

	async def create(
			self: Self,
			user_id: PositiveInt,
			chats_count: PositiveInt,
			messages_count: PositiveInt,
			data: defaultdict,
			date: str,
			filename: str,
			session: AsyncSession,
	) -> UserStats:	...

	async def read(
			self: Self,
			user_id: PositiveInt,
			session: AsyncSession,
	) -> UserStats | None:	...

	async def delete(
			self: Self,
			user_stats_id: PositiveInt,
			session: AsyncSession,
	) -> None:	...


class UserStatsRepositoryImpl:
	"""
	"""

	async def create(
			self: Self,
			user_id: PositiveInt,
			chats_count: PositiveInt,
			messages_count: PositiveInt,
			data: defaultdict,
			date: str,
			filename: str,
			session: AsyncSession,
	) -> UserStats:
		"""
		"""
		user_stats = UserStats(
			chats_count=chats_count,
			messages_count=messages_count,
			data=data or {},
			date=date,
			user_id=user_id,
			report_filepath=filename,
		)
		session.add(user_stats)
		await session.commit()

		return user_stats

	async def read(
			self: Self,
			user_id: PositiveInt,
			session: AsyncSession,
	) -> UserStats | None:
		"""
		"""
		return await session.get(
			entity=UserStats,
			ident=user_id
		)

	async def delete(
			self: Self,
			user_stats_id: PositiveInt,
			session: AsyncSession,
	) -> None:
		"""
		"""
		await session.execute(
			delete(
				UserStats
			).where(
				UserStats.id == user_stats_id,
			)
		)
		await session.commit()


class PostgresRepositoryProtocol(Protocol):
	"""
	"""

	def __init__(
			self: Self,
			user_stats_repository: UserStatsRepositoryProtocol,
			chat_repository: ChatRepositoryProtocol,
			chat_stats_repository: ChatStatsRepositoryProtocol,
			message_stats_repository: MessageStatsRepositoryProtocol,
	) -> None:	...

	async def read_hourly_message_stats(
			self: Self,
			session: AsyncSession,
			user_tg_id: PositiveInt,
			hourly_stats_date: str,
	) -> Sequence[MessageStats]:	...

	async def create_user_stats(
			self: Self,
			user_tg_id: PositiveInt,
			date: str,
			user_stats: UserStats | None,
			filename: str,
	) -> UserStats:	...

	async def create_chat_stats(
			self: Self,
			chat_tg_id: PositiveInt,
			date: str,
			chat_stats: ChatStats | None,
			filename: str,
	) -> ChatStats:	...

	async def read_user_stats(
			self: Self,
			user_tg_id: PositiveInt,
			date: str,
	) -> UserStats | None:	...

	async def read_chat_stats(
			self: Self,
			chat_tg_id: NegativeInt,
			date: str,
	) -> ChatStats | None:	...


class PostgresRepositoryImpl:
	"""
	"""

	def __init__(
			self: Self,
			user_stats_repository: UserStatsRepositoryProtocol,
			chat_repository: ChatRepositoryProtocol,
			chat_stats_repository: ChatStatsRepositoryProtocol,
			message_stats_repository: MessageStatsRepositoryProtocol,
	) -> None:
		self.user_stats_repository = user_stats_repository
		self.chat_repository = chat_repository
		self.chat_stats_repository = chat_stats_repository
		self.message_stats_repository = message_stats_repository

	async def create_user_stats(
			self: Self,
			user_tg_id: PositiveInt,
			date: str,
			user_stats: UserStats | None,
			filename: str,
	) -> UserStats:
		"""
		"""
		async with Postgres.session_maker() as session:
			if user_stats:
				# XXX (ames0k0): Daily cache <not hourly>
				await self.user_stats_repository.delete(
					user_stats_id=user_stats.id,
					session=session,
				)

			daily_message_stats = await self.message_stats_repository.read(
				user_id=user_tg_id,
				chat_id=None,
				date=date,
				session=session,
			)

			gen_data = defaultdict(dict)
			all_chats_count = 0
			all_messages_count = 0

			for chat_id, chat_ms in groupby(
					daily_message_stats,
					key=lambda x: x.chat_id,
			):
				messages_count = {}
				all_chats_count += 1
				chat = await self.chat_repository.read(
					chat_id=chat_id,
					session=session,
				)
				if not chat:
					# NOTE (ames0k0): It should be in the database (`src__events_analyzer`)
					# TODO (ames0k0): Add to the database ?!
					continue

				for ms in chat_ms:
					all_messages_count += ms.message_count
					messages_count[parse_h_from_dt(ms.date)] = ms.message_count

				gen_data[chat_id]["chat_name"] = chat.full_name
				gen_data[chat_id]["data"] = messages_count

			return await self.user_stats_repository.create(
				user_id=user_tg_id,
				chats_count=all_chats_count,
				messages_count=all_messages_count,
				data=gen_data,
				date=date,
				filename=filename,
				session=session,
			)

	async def create_chat_stats(
			self: Self,
			chat_tg_id: PositiveInt,
			date: str,
			chat_stats: ChatStats | None,
			filename: str,
	) -> ChatStats:
		"""
		"""
		async with Postgres.session_maker() as session:
			if chat_stats:
				await self.chat_stats_repository.delete(
					chat_stats_id=chat_stats.id,
					session=session,
				)

			chat = await self.chat_repository.read(
				chat_id=chat_tg_id,
				session=session,
			)
			daily_message_stats = await self.message_stats_repository.read(
				user_id=None,
				chat_id=chat_tg_id,
				date=date,
				session=session,
			)

			gen_data = {
				"chat_name": chat.full_name,
				"users_count": 0,
				"messages_count": 0,
				"data": {},
			}
			all_users_count = set()
			all_messages_count = 0

			for date_value, date_ms in groupby(
					daily_message_stats,
					key=lambda x: parse_h_from_dt(x.date),
			):
				users_count = set()
				messages_count = 0

				for ms in date_ms:
					users_count.add(ms.user_id)
					messages_count += ms.message_count

				all_messages_count += messages_count
				gen_data["data"][date_value] = {
					"users_count": len(users_count),
					"messages_count": messages_count,
				}
				all_users_count.update(users_count)
				users_count.clear()

			gen_data["users_count"] = len(all_users_count)
			gen_data["messages_count"] = all_messages_count

		return await self.chat_stats_repository.create(
			chat_id=chat_tg_id,
			date=date,
			users_count=len(all_users_count),
			messages_count=all_messages_count,
			data=gen_data,
			filename=filename,
			session=session,
		)

	async def read_user_stats(
			self: Self,
			user_tg_id: PositiveInt,
			date: str,
	) -> UserStats | None:
		"""
		"""
		async with Postgres.session_maker() as session:
			return await session.scalar(
				select(
					UserStats
				).where(
					UserStats.user_id == user_tg_id,
					UserStats.date == date,
				)
			)

	async def read_chat_stats(
			self: Self,
			chat_tg_id: NegativeInt,
			date: str,
	) -> ChatStats | None:
		"""
		"""
		async with Postgres.session_maker() as session:
			return await session.scalar(
				select(
					ChatStats
				).where(
					ChatStats.chat_id == chat_tg_id,
					ChatStats.date == date,
				)
			)

	async def update_chat_stats(
			self: Self,
			chat_id: NegativeInt,
			date: str,
			session: AsyncSession,
	) -> None:
		"""
		MessageStats will be generated later
			-> MessageStats.date.startswith(stats_date)	-> [d] all_users
			-> MessageStats.date.endswith(stats_hours)	-> [h] all_users
		"""
		stats_date, stats_hour = date.split(" ")
		chat_stats = await self.chat_stats_repository.init(
			chat_id=chat_id,
			date=stats_date,
			session=session,
		)
		# message_stats_date = self.
		# message_stats_hour =


def get_message_stats_repository() -> MessageStatsRepositoryProtocol:
	"""
	"""
	return MessageStatsRepositoryImpl()


def get_user_stats_repository() -> UserStatsRepositoryProtocol:
	"""
	"""
	return UserStatsRepositoryImpl()


def get_chat_repository() -> ChatRepositoryProtocol:
	"""
	"""
	return ChatRepositoryImpl()


def get_chat_stats_repository() -> ChatStatsRepositoryProtocol:
	"""
	"""
	return ChatStatsRepositoryImpl()


def get_postgres_repository() -> PostgresRepositoryProtocol:
	"""
	"""
	return PostgresRepositoryImpl(
		user_stats_repository=UserStatsRepository,
		chat_repository=ChatRepository,
		chat_stats_repository=ChatStatsRepository,
		message_stats_repository=MessageStatsRepository,
	)


MessageStatsRepository = get_message_stats_repository()
UserStatsRepository = get_user_stats_repository()
ChatRepository = get_chat_repository()
ChatStatsRepository = get_chat_stats_repository()
PostgresRepository = get_postgres_repository()