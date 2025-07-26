from typing import Protocol
from typing import Self
from typing import AsyncGenerator
from contextlib import asynccontextmanager

from pydantic import PositiveInt
from pydantic import NegativeInt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from stbcore.schemas.kafka import TelegramUserObjectSchema
from stbcore.schemas.kafka import TelegramChatObjectSchema
from stbcore.schemas.kafka import TelegramMessageEventSchema

from stbcore.infra.postgres import Postgres
from stbcore.models.user import User
from stbcore.models.user import UserSettings
from stbcore.models.message import Message
from stbcore.models.message import MessageStats
from stbcore.models.chat import Chat
from stbcore.models.chat import ChatSettings


__all__ = (
	"PostgresRepositoryProtocol",
	"PostgresRepository",
)


class MessageStatsRepositoryProtocol(Protocol):
	"""
	"""

	async def create(
			self: Self,
			payload: TelegramMessageEventSchema,
			session: AsyncSession,
	) -> MessageStats:	...

	async def read(
			self: Self,
			payload: TelegramMessageEventSchema,
			session: AsyncSession,
	) -> MessageStats | None:	...

	async def init(
			self: Self,
			payload: TelegramMessageEventSchema,
			session: AsyncSession,
	) -> MessageStats:	...


class MessageStatsRepositoryImpl:
	"""
	"""

	async def create(
			self: Self,
			payload: TelegramMessageEventSchema,
			session: AsyncSession,
	) -> MessageStats:
		"""
		"""
		message_stats = MessageStats(
			user_id=payload.user.tg_id,
			chat_id=payload.chat.tg_id,
			date=payload.message.date,
		)
		session.add(message_stats)
		await session.commit()

		return message_stats

	async def read(
			self: Self,
			payload: TelegramMessageEventSchema,
			session: AsyncSession,
	) -> MessageStats | None:
		"""
		"""
		return await session.scalar(
			select(
				MessageStats
			).where(
				MessageStats.user_id == payload.user.tg_id,
				MessageStats.chat_id == payload.chat.tg_id,
			)
		)

	async def init(
			self: Self,
			payload: TelegramMessageEventSchema,
			session: AsyncSession,
	) -> MessageStats:
		"""
		"""
		message_stats = await self.read(
			payload=payload,
			session=session
		)
		if not message_stats:
			message_stats = await self.create(
				payload=payload,
				session=session,
			)

		return message_stats


class UserSettingsRepositoryProtocol(Protocol):
	"""
	"""

	async def create(
			self: Self,
			user_id: PositiveInt,
			session: AsyncSession,
	) -> None:	...


class UserSettingsRepositoryImpl:
	"""
	"""

	async def create(
			self: Self,
			user_id: PositiveInt,
			session: AsyncSession,
	) -> None:
		"""
		"""
		session.add(
			UserSettings(user_id=user_id),
		)
		await session.commit()


class UserRepositoryProtocol(Protocol):
	"""
	"""

	def __init__(
			self: Self,
			user_settings_repository: UserSettingsRepositoryProtocol,
	) -> None:	...

	async def create(
			self: Self,
			user_tg_id: PositiveInt,
			session: AsyncSession,
	) -> User:	...

	async def read(
			self: Self,
			user_tg_id: PositiveInt,
			session: AsyncSession,
	) -> User | None:	...

	async def init(
			self: Self,
			payload: TelegramUserObjectSchema,
			session: AsyncSession,
	) -> User:	...


class UserRepositoryImpl:
	"""
	"""

	def __init__(
			self: Self,
			user_settings_repository: UserSettingsRepositoryProtocol,
	) -> None:
		self.user_settings_repository = user_settings_repository

	async def create(
			self: Self,
			payload: TelegramUserObjectSchema,
			session: AsyncSession,
	) -> User:
		"""
		"""
		user = User(
			id=payload.tg_id,
			username=payload.username,
			full_name=payload.full_name,
		)
		session.add(user)
		await session.commit()

		return user

	async def read(
			self: Self,
			payload: TelegramUserObjectSchema,
			session: AsyncSession,
	) -> User | None:
		"""
		"""
		return await session.scalar(
			select(
				User,
			).where(
				User.id == payload.tg_id,
			).options(
				selectinload(User.message_settings),
			)
		)

	async def init(
	 		self: Self,
			payload: TelegramUserObjectSchema,
			session: AsyncSession,
	) -> User:
		"""
		"""
		user = await self.read(payload=payload, session=session)
		if user:
			return user

		user = await self.create(
			payload=payload,
			session=session,
		)
		await self.user_settings_repository.create(
			user_id=user.id,
			session=session,
		)

		return await self.read(payload=payload, session=session)


class ChatSettingsRepositoryProtocol(Protocol):
	"""
	"""

	async def create(
			self: Self,
			chat_id: NegativeInt,
			session: AsyncSession,
	) -> None:	...


class ChatSettingsRepositoryImpl:
	"""
	"""

	async def create(
			self: Self,
			chat_id: NegativeInt,
			session: AsyncGenerator,
	) -> None:
		"""
		"""
		session.add(
			ChatSettings(chat_id=chat_id),
		)
		await session.commit()


class ChatRepositoryProtocol(Protocol):
	"""
	"""

	def __init__(
			self: Self,
			chat_settings_repository: ChatSettingsRepositoryProtocol,
	) -> None:	...

	async def create(
			self: Self,
			payload: TelegramChatObjectSchema,
			session: AsyncSession,
	) -> Chat:	...

	async def read(
			self: Self,
			payload: TelegramChatObjectSchema,
			session: AsyncSession,
	) -> Chat | None:	...

	async def init(
			self: Self,
			payload: TelegramChatObjectSchema,
			session: AsyncSession,
	) -> Chat:	...


class ChatRepositoryImpl:
	"""
	"""

	def __init__(
			self: Self,
			chat_settings_repository: ChatSettingsRepositoryProtocol,
	) -> None:
		self.chat_settings_repository = chat_settings_repository

	async def create(
			self: Self,
			payload: TelegramChatObjectSchema,
			session: AsyncSession,
	) -> Chat:
		"""
		"""
		chat = Chat(
			id=payload.tg_id,
			username=payload.username,
			full_name=payload.full_name,
		)
		session.add(chat)
		await session.commit()

		return chat

	async def read(
			self: Self,
			payload: TelegramChatObjectSchema,
			session: AsyncSession,
	) -> Chat | None:
		"""
		"""
		return await session.scalar(
			select(
				Chat,
			).where(
				Chat.id == payload.tg_id,
			).options(
				selectinload(Chat.message_settings),
			)
		)

	async def init(
	 		self: Self,
			payload: TelegramChatObjectSchema,
			session: AsyncSession,
	) -> Chat:
		"""
		"""
		chat = await self.read(payload=payload, session=session)
		if chat:
			return chat

		chat = await self.create(
			payload=payload,
			session=session,
		)
		await self.chat_settings_repository.create(
			chat_id=chat.id,
			session=session,
		)

		return await self.read(payload=payload, session=session)


class PostgresRepositoryProtocol(Protocol):
	"""
	"""

	def __init__(
			self: Self,
			user_repository: UserRepositoryProtocol,
			chat_repository: ChatRepositoryProtocol,
			chat_settings_repository: ChatSettingsRepositoryProtocol,
			message_stats_repository: MessageStatsRepositoryProtocol,
	) -> None:	...

	async def session_context() -> AsyncGenerator[AsyncSession, None]:	...

	async def init_user(
			self: Self,
			payload: TelegramUserObjectSchema,
			session: AsyncSession,
	) -> User:	...

	async def init_chat(
			self: Self,
			payload: TelegramChatObjectSchema,
			session: AsyncSession,
	) -> Chat:	...

	async def update_message_stats(
			self: Self,
			payload: TelegramMessageEventSchema,
			session: AsyncSession,
	) -> None:	...


class PostgresRepositoryImpl:
	"""
	"""

	def __init__(
			self: Self,
			user_repository: UserRepositoryProtocol,
			chat_repository: ChatRepositoryProtocol,
			message_stats_repository: MessageStatsRepositoryProtocol,
	) -> None:
		self.user_repository = user_repository
		self.chat_repository = chat_repository
		self.message_stats_repository = message_stats_repository

	@staticmethod
	@asynccontextmanager
	async def session_context() -> AsyncGenerator[AsyncSession, None]:
		async with Postgres.session_maker() as session:
			yield session

	async def init_user(
			self: Self,
			payload: TelegramUserObjectSchema,
			session: AsyncSession,
	) -> User:
		"""
		"""
		return await self.user_repository.init(
			payload=payload,
			session=session,
		)

	async def init_chat(
			self: Self,
			payload: TelegramChatObjectSchema,
			session: AsyncSession,
	) -> Chat:
		"""
		"""
		return await self.chat_repository.init(
			payload=payload,
			session=session,
		)

	async def update_message_stats(
			self: Self,
			payload: TelegramMessageEventSchema,
			session: AsyncSession,
	) -> None:
		"""
		"""
		message_stats = await self.message_stats_repository.init(
			payload=payload,
			session=session,
		)
		message_stats.message_count += 1
		await session.commit()


def get_user_repository() -> UserRepositoryProtocol:
	"""
	"""
	return UserRepositoryImpl(
		user_settings_repository=UserSettingsRepository,
	)


def get_user_settings_repository() -> UserSettingsRepositoryProtocol:
	"""
	"""
	return UserSettingsRepositoryImpl()


def get_chat_repository() -> ChatRepositoryProtocol:
	"""
	"""
	return ChatRepositoryImpl(
		chat_settings_repository=ChatSettingsRepository,
	)


def get_chat_settings_repository() -> ChatSettingsRepositoryProtocol:
	"""
	"""
	return ChatSettingsRepositoryImpl()


def get_message_repository() -> MessageStatsRepositoryProtocol:
	"""
	"""
	return MessageStatsRepositoryImpl()


def get_postgres_repository() -> PostgresRepositoryProtocol:
	"""
	"""
	return PostgresRepositoryImpl(
		user_repository=UserRepository,
		chat_repository=ChatRepository,
		message_stats_repository=MessageStatsRepository,
	)


UserSettingsRepository = get_user_settings_repository()
UserRepository = get_user_repository()
ChatSettingsRepository = get_chat_settings_repository()
ChatRepository = get_chat_repository()
MessageStatsRepository = get_message_repository()
PostgresRepository = get_postgres_repository()