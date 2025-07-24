from typing import Protocol
from typing import Self

from stbcore.schemas.kafka import MessageEventSchema

from repositories.postgres import PostgresRepositoryProtocol
from repositories.postgres import PostgresRepository


class EventsAnalyzerServiceProtocol(Protocol):
	"""
	"""

	def __init__(
			self: Self,
			postgres_repository: PostgresRepositoryProtocol,
	) -> None:	...

	async def message_events_analyzer(
			self: Self,
			payload: MessageEventSchema,
	) -> None:	...


class EventsAnalyzerServiceImpl:
	"""
	"""

	def __init__(
			self: Self,
			postgres_repository: PostgresRepositoryProtocol,
	) -> None:
		self.postgres_repository = postgres_repository

	async def message_events_analyzer(
			self: Self,
			payload: MessageEventSchema,
	) -> None:
		""" Updated the MessageStats, UserStats
		"""
		if payload.user_tg_id == payload.chat_tg_id:
			return

		user = await self.postgres_repository.init_user(
			user_tg_id=payload.user_tg_id,
		)
		chat = await self.postgres_repository.init_chat(
			chat_tg_id=payload.chat_tg_id,
		)

		if any((
			user.message_settings.save_stats,
			chat.message_settings.save_stats,
		)):
			await self.postgres_repository.update_message_stats(
				user_id=user.id,
				chat_id=chat.id,
				date=payload.date,
			)


def get_events_analyzer_repository() -> EventsAnalyzerServiceProtocol:
	"""
	"""
	return EventsAnalyzerServiceImpl(
		postgres_repository=PostgresRepository,
	)


EventsAnalyzerService = get_events_analyzer_repository()