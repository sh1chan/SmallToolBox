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
			session: AsyncSession,
	) -> ChatStats:	...

	async def read(
			self: Self,
			chat_id: NegativeInt,
			session: AsyncSession,
	) -> ChatStats | None:	...


class ChatStatsRepositoryImpl:
	"""
	"""

	async def create(
			self: Self,
			chat_id: NegativeInt,
			date: str,
			session: AsyncSession,
	) -> ChatStats:
		"""
		"""
		# NOTE (ames0k0)
		#	- `stb__stats_generator` tries to delete the `fake` report filepath
		chat_stats = ChatStats(
			chat_id=chat_id,
			date=date,
			repost_filepath="fake",
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
			report_filepath="fake",
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
				UserStats.id==user_stats_id,
			)
		)
		await session.commit()


class UserRepositoryProtocol(Protocol):
	"""
	"""

	def __init__(
			self: Self,
			user_stats_repository: UserStatsRepositoryProtocol,
	) -> None:	...

	async def delete_user_stats(
			self: Self,
			user_stats_id: PositiveInt,
			session: AsyncSession,
	) -> None:	...


class UserRepositoryImpl:
	"""
	"""

	def __init__(
			self: Self,
			user_stats_repository: UserStatsRepositoryProtocol,
	) -> None:
		self.user_stats_repository = user_stats_repository

	async def delete_user_stats(
			self: Self,
			user_stats_id: PositiveInt,
			session: AsyncSession,
	) -> None:
		"""
		"""
		await self.user_stats_repository.delete(
			user_stats_id=user_stats_id,
			session=session,
		)


class PostgresRepositoryProtocol(Protocol):
	"""
	"""

	def __init__(
			self: Self,
			user_stats_repository: UserStatsRepositoryProtocol,
			chat_repository: ChatStatsRepositoryProtocol,
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
	) -> UserStats:	...

	async def read_user_stats(
			self: Self,
			user_tg_id: PositiveInt,
			date: str,
	) -> UserStats | None:	...

	async def update_user_stats_filename(self: Self, user_stats_id: PositiveInt, filename: str) -> None:	...

	async def update_chat_stats(
			self: Self,
			chat_id: NegativeInt,
			date: str,
			session: AsyncSession,
	) -> None:	...


class PostgresRepositoryImpl:
	"""
	"""

	def __init__(
			self: Self,
			user_stats_repository: UserStatsRepositoryProtocol,
			chat_repository: ChatStatsRepositoryProtocol,
			message_stats_repository: MessageStatsRepositoryProtocol,
	) -> None:
		self.user_stats_repository = user_stats_repository
		self.chat_repository = chat_repository
		self.message_stats_repository = message_stats_repository

	async def read_hourly_message_stats(
			self: Self,
			session: AsyncSession,
			user_tg_id: PositiveInt,
			hourly_stats_date: str
	) -> Sequence[MessageStats]:
		"""
		"""
		return (await session.execute(
			select(
				MessageStats
			).where(
				MessageStats.user_id == user_tg_id,
				MessageStats.date == hourly_stats_date,
			)
		)).scalars()

	async def create_user_stats(
			self: Self,
			user_tg_id: PositiveInt,
			date: str,
			user_stats: UserStats | None,
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
				all_chats_count += 1
				chat = await self.chat_repository.read(
					chat_id=chat_id,
					session=session,
				)
				if not chat:
					# NOTE (ames0k0): It should be in the database (`src__events_analyzer`)
					# TODO (ames0k0): Add to the database ?!
					continue

				messages_count = {}
				for ms in chat_ms:
					all_messages_count += ms.message_count
					message_h_from_date = ms.date.split(" ")[1].split(":")[0]
					messages_count[int(message_h_from_date)] = ms.message_count

				gen_data[chat_id]["chat_name"] = chat.full_name
				gen_data[chat_id]["data"] = messages_count

			return await self.user_stats_repository.create(
				user_id=user_tg_id,
				chats_count=all_chats_count,
				messages_count=all_messages_count,
				data=gen_data,
				date=date,
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

	async def update_user_stats_filename(self: Self, user_stats_id: PositiveInt, filename: str) -> None:
		"""
		"""
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


def get_user_repository() -> UserRepositoryProtocol:
	"""
	"""
	return UserRepositoryImpl(
		user_stats_repository=UserStatsRepository,
	)


def get_chat_repository() -> ChatRepositoryProtocol:
	"""
	"""
	return ChatRepositoryImpl()


def get_postgres_repository() -> PostgresRepositoryProtocol:
	"""
	"""
	return PostgresRepositoryImpl(
		user_stats_repository=UserStatsRepository,
		chat_repository=ChatRepository,
		message_stats_repository=MessageStatsRepository,
	)


MessageStatsRepository = get_message_stats_repository()
UserStatsRepository = get_user_stats_repository()
UserRepository = get_user_repository()
ChatRepository = get_chat_repository()
PostgresRepository = get_postgres_repository()