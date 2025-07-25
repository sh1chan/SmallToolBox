from typing import Protocol
from typing import Self

from stbcore.schemas.kafka import MessageEventSchema

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
			payload: MessageEventSchema,
	) -> None:	...


class EventsAnalyzerRepositoryImpl:
	"""
	"""

	def __init__(
			self: Self,
			postgres_repository: PostgresRepositoryProtocol
	) -> None:
		self.postgres_repository = postgres_repository

	async def message_events_analyzer(
			self: Self,
			payload: MessageEventSchema,
	) -> None:
		"""
		"""
		if payload.user_tg_id == payload.chat_tg_id:
			return

		async with self.postgres_repository.session_context() as session:
			user = await self.user_repository.init_user(
				user_tg_id=payload.user_tg_id,
				session=session,
			)
			chat = await self.chat_repository.init_chat(
				chat_tg_id=payload.chat_tg_id,
				session=session,
			)

			if not any((
				user.message_settings.save_stats,
				chat.message_settings.save_stats,
			)):
				return

			await self.message_repository.update_message_stats(
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
	)


EventsAnalyzerRepository = get_events_analyzer_repository()