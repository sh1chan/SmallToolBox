from typing import Protocol
from typing import Self
from typing import AsyncGenerator
from contextlib import asynccontextmanager

from pydantic import PositiveInt
from pydantic import NegativeInt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from stbcore.infra.postgres import Postgres
from stbcore.models.user import User
from stbcore.models.user import UserSettings
from stbcore.models.user import UserStats
from stbcore.models.message import Message
from stbcore.models.message import MessageStats
from stbcore.models.chat import Chat
from stbcore.models.chat import ChatSettings
from stbcore.models.chat import ChatStats


__all__ = (
	"PostgresRepositoryProtocol",
	"PostgresRepository",
)


class MessageRepositoryProtocol(Protocol):
	"""
	"""

	async def create_message_stats(
			self: Self,
			user_id: PositiveInt,
			chat_id: NegativeInt,
			date: str,
			session: AsyncSession,
	) -> MessageStats:	...

	async def read_message_stats(
			self: Self,
			user_id: PositiveInt,
			chat_id: NegativeInt,
			session: AsyncSession,
	) -> MessageStats | None:	...

	async def init_message_stats(
			self: Self,
			user_id: PositiveInt,
			chat_id: NegativeInt,
			date: str,
			session: AsyncSession,
	) -> MessageStats:	...

	async def update_message_stats(
			self: Self,
			user_id: PositiveInt,
			chat_id: NegativeInt,
			date: str,
			session: AsyncSession,
	) -> None:	...


class MessageRepositoryImpl:
	"""
	"""

	async def create_message_stats(
			self: Self,
			user_id: PositiveInt,
			chat_id: NegativeInt,
			date: str,
			session: AsyncSession,
	) -> MessageStats:
		"""
		"""
		message_stats = MessageStats(
			user_id=user_id,
			chat_id=chat_id,
			date=date,
		)
		session.add(message_stats)
		await session.commit()

		return message_stats

	async def read_message_stats(
			self: Self,
			user_id: PositiveInt,
			chat_id: NegativeInt,
			session: AsyncSession,
	) -> MessageStats | None:
		"""
		"""
		return await session.scalar(
			select(
				MessageStats
			).where(
				MessageStats.user_id == user_id,
				MessageStats.chat_id == chat_id,
			)
		)

	async def init_message_stats(
			self: Self,
			user_id: PositiveInt,
			chat_id: NegativeInt,
			date: str,
			session: AsyncSession,
	) -> MessageStats:
		"""
		"""
		message_stats = await self.read_message_stats(
			user_id=user_id,
			chat_id=chat_id,
			session=session
		)
		if not message_stats:
			message_stats = await self.create_message_stats(
				user_id=user_id,
				chat_id=chat_id,
				date=date,
				session=session,
			)

		return message_stats

	async def update_message_stats(
			self: Self,
			user_id: PositiveInt,
			chat_id: NegativeInt,
			date: str,
			session: AsyncSession,
	) -> None:
		"""
		"""
		message_stats = await self.init_message_stats(
			user_id=user_id,
			chat_id=chat_id,
			date=date,
			session=session,
		)
		message_stats.message_count += 1
		await session.commit()


class UserRepositoryProtocol(Protocol):
	"""
	"""

	async def create_user(
			self: Self,
			user_tg_id: PositiveInt,
			session: AsyncSession,
	) -> User:	...

	async def create_user_settings(
			self: Self,
			user_id: PositiveInt,
			session: AsyncSession,
	) -> None:	...

	async def read_user(
			self: Self,
			user_tg_id: PositiveInt,
			session: AsyncSession,
	) -> User | None:	...

	async def init_user(
			self: Self,
			user_tg_id: PositiveInt,
			session: AsyncSession,
	) -> User:	...


class UserRepositoryImpl:
	"""
	"""

	async def create_user(
			self: Self,
			user_tg_id: PositiveInt,
			session: AsyncSession,
	) -> User:
		"""
		"""
		user = User(
			id=user_tg_id,
			full_name="Not Set",
		)
		session.add(user)
		await session.commit()

		return user

	async def create_user_settings(
			self: Self,
			user_id: PositiveInt,
			session: AsyncSession,
	) -> None:
		"""
		"""
		session.add(UserSettings(user_id=user_id))
		await session.commit()

	async def read_user(
			self: Self,
			user_tg_id: PositiveInt,
			session: AsyncSession,
	) -> User | None:
		"""
		"""
		return await session.get(entity=User, ident=user_tg_id)

	async def init_user(
	 		self: Self,
			user_tg_id: PositiveInt,
			session: AsyncSession,
	) -> User:
		"""
		"""
		user = await self.read_user(user_tg_id=user_tg_id, session=session)
		if user:
			return user

		user = await self.create_user(
			user_tg_id=user_tg_id,
			session=session,
		)
		await self.create_user_settings(
			user_id=user.id,
			session=session,
		)

		return user


class ChatRepositoryProtocol(Protocol):
	"""
	"""

	async def create_chat(
			self: Self,
			chat_tg_id: NegativeInt,
			session: AsyncSession,
	) -> Chat:	...

	async def create_chat_settings(
			self: Self,
			chat_id: NegativeInt,
			session: AsyncSession,
	) -> None:	...

	async def read_chat(
			self: Self,
			chat_tg_id: NegativeInt,
			session: AsyncSession,
	) -> Chat | None:	...

	async def init_chat(
			self: Self,
			chat_tg_id: NegativeInt,
			session: AsyncSession,
	) -> Chat:	...


class ChatRepositoryImpl:
	"""
	"""

	async def create_chat(
			self: Self,
			chat_tg_id: NegativeInt,
			session: AsyncSession,
	) -> Chat:
		"""
		"""
		chat = Chat(
			id=chat_tg_id,
			full_name="Not Set",
		)
		session.add(chat)
		await session.commit()

		return chat

	async def create_chat_settings(
			self: Self,
			chat_id: NegativeInt,
			session: AsyncSession,
	) -> None:
		"""
		"""
		session.add(ChatSettings(chat_id=chat_id))
		await session.commit()

	async def read_chat(
			self: Self,
			chat_tg_id: NegativeInt,
			session: AsyncSession,
	) -> Chat | None:
		"""
		"""
		return await session.get(entity=Chat, ident=chat_tg_id)

	async def init_chat(
	 		self: Self,
			chat_tg_id: NegativeInt,
			session: AsyncSession,
	) -> Chat:
		"""
		"""
		chat = await self.read_chat(chat_tg_id=chat_tg_id, session=session)
		if chat:
			return chat

		chat = await self.create_chat(
			chat_tg_id=chat_tg_id,
			session=session,
		)
		await self.create_chat_settings(
			chat_id=chat.id,
			session=session,
		)

		return chat


class PostgresRepositoryProtocol(Protocol):
	"""
	"""

	async def session_context() -> AsyncGenerator[AsyncSession, None]:	...


class PostgresRepositoryImpl:
	"""
	"""

	@staticmethod
	@asynccontextmanager
	async def session_context() -> AsyncGenerator[AsyncSession, None]:
		async with Postgres.session_maker() as session:
			yield session


def get_user_repository() -> UserRepositoryProtocol:
	"""
	"""
	return UserRepositoryImpl()


def get_chat_repository() -> ChatRepositoryProtocol:
	"""
	"""
	return ChatRepositoryImpl()


def get_message_repository() -> MessageRepositoryProtocol:
	"""
	"""
	return MessageRepositoryImpl()


def get_postgres_repository() -> PostgresRepositoryProtocol:
	"""
	"""
	return PostgresRepositoryImpl()


UserRepository = get_user_repository()
ChatRepository = get_chat_repository()
MessageRepository = get_message_repository()
PostgresRepository = get_postgres_repository()