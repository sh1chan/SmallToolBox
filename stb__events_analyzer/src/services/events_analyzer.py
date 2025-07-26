from typing import Protocol
from typing import Self

from stbcore.schemas.kafka import TelegramMessageEventSchema

from repositories.events_analyzer import EventsAnalyzerRepository
from repositories.events_analyzer import EventsAnalyzerRepositoryProtocol


class EventsAnalyzerServiceProtocol(Protocol):
	"""
	"""

	def __init__(
			self: Self,
			events_analyzer_repository: EventsAnalyzerRepositoryProtocol,
	) -> None:	...

	async def message_events_analyzer(
			self: Self,
			payload: TelegramMessageEventSchema,
	) -> None:	...


class EventsAnalyzerServiceImpl:
	"""
	"""

	def __init__(
			self: Self,
			events_analyzer_repository: EventsAnalyzerRepositoryProtocol,
	) -> None:
		self.events_analyzer_repository = events_analyzer_repository

	async def message_events_analyzer(
			self: Self,
			payload: TelegramMessageEventSchema,
	) -> None:
		""" Updated the MessageStats, UserStats
		"""
		await self.events_analyzer_repository.message_events_analyzer(
			payload=payload,
		)


def get_events_analyzer_repository() -> EventsAnalyzerServiceProtocol:
	"""
	"""
	return EventsAnalyzerServiceImpl(
		events_analyzer_repository=EventsAnalyzerRepository,
	)


EventsAnalyzerService = get_events_analyzer_repository()