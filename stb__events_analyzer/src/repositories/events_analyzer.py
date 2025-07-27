from typing import Protocol
from typing import Self

from stbcore.schemas.kafka import TelegramMessageEventSchema

from .postgres import PostgresRepository
from .postgres import PostgresRepositoryProtocol


class EventsAnalyzerRepositoryProtocol(Protocol):
	"""
	"""

	def __init__(
			self: Self,
			postgres_repository: PostgresRepositoryProtocol,
	) -> None:	...

	async def message_events_analyzer(
			self: Self,
			payload: TelegramMessageEventSchema,
	) -> None:	...


class EventsAnalyzerRepositoryImpl:
	"""
	"""

	def __init__(
			self: Self,
			postgres_repository: PostgresRepositoryProtocol,
	) -> None:
		self.postgres_repository = postgres_repository

	async def message_events_analyzer(
			self: Self,
			payload: TelegramMessageEventSchema,
	) -> None:
		"""
		-> User
			-> UserSettings
				-> Message
		-> Chat
			-> ChatSettings
		-> MessageStats
		"""
		if payload.user.tg_id == payload.chat.tg_id:
			return

		async with self.postgres_repository.session_context() as session:
			user = await self.postgres_repository.init_user(
				payload=payload.user,
				session=session,
			)
			chat = await self.postgres_repository.init_chat(
				payload=payload.chat,
				session=session,
			)

			if user.message_settings.save_messages:
				await self.postgres_repository.create_message(
					payload=payload,
					session=session,
				)

			if not any((
				user.message_settings.save_stats,
				chat.message_settings.save_stats,
			)):
				return

			await self.postgres_repository.update_message_stats(
				payload=payload,
				session=session,
			)


def get_events_analyzer_repository() -> EventsAnalyzerRepositoryProtocol:
	"""
	"""
	return EventsAnalyzerRepositoryImpl(
		postgres_repository=PostgresRepository,
	)


EventsAnalyzerRepository = get_events_analyzer_repository()