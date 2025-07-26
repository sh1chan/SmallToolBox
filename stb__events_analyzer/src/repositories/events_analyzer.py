from typing import Protocol
from typing import Self

from stbcore.schemas.kafka import MessageEventSchema

from .postgres import PostgresRepository
from .postgres import PostgresRepositoryProtocol
from .postgres import UserRepositoryProtocol
from .postgres import UserRepository
from .postgres import ChatRepositoryProtocol
from .postgres import ChatRepository


class EventsAnalyzerRepositoryProtocol(Protocol):
	"""
	"""

	def __init__(
			self: Self,
			postgres_repository: PostgresRepositoryProtocol,
			user_repository: UserRepositoryProtocol,
			chat_repository: ChatRepositoryProtocol,
	) -> None:	...

	async def message_events_analyzer(
			self: Self,
			payload: MessageEventSchema,
	) -> None:	...


class EventsAnalyzerRepositoryImpl:
	"""
	"""

	def __init__(
			self: Self,
			postgres_repository: PostgresRepositoryProtocol,
			user_repository: UserRepositoryProtocol,
			chat_repository: ChatRepositoryProtocol,
	) -> None:
		self.postgres_repository = postgres_repository
		self.user_repository = user_repository
		self.chat_repository = chat_repository

	async def message_events_analyzer(
			self: Self,
			payload: MessageEventSchema,
	) -> None:
		"""
		MessageStats
			-> User
				-> UserSettings
					-> Message
			-> Chat
				-> ChatSettings
		"""
		if payload.user_tg_id == payload.chat_tg_id:
			return

		async with self.postgres_repository.session_context() as session:
			user = await self.user_repository.init(
				user_tg_id=payload.user_tg_id,
				session=session,
			)
			chat = await self.chat_repository.init(
				chat_tg_id=payload.chat_tg_id,
				session=session,
			)

			if user.message_settings.save_messages:
				# TODO (ames0k0): Implement
				pass

			if not any((
				user.message_settings.save_stats,
				chat.message_settings.save_stats,
			)):
				return

			await self.postgres_repository.update_message_stats(
				user_id=user.id,
				chat_id=chat.id,
				date=payload.date,
				session=session,
			)


def get_events_analyzer_repository() -> EventsAnalyzerRepositoryProtocol:
	"""
	"""
	return EventsAnalyzerRepositoryImpl(
		postgres_repository=PostgresRepository,
		user_repository=UserRepository,
		chat_repository=ChatRepository,
	)


EventsAnalyzerRepository = get_events_analyzer_repository()