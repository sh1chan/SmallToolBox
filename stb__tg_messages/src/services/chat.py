from typing import Protocol
from typing import Self

from stbcore.schemas.rabbit import GenerateStatsSchema

from repositories.redis import RedisRepositoryProtocol
from repositories.redis import RedisRepository
from repositories.rabbit import RabbitRepositoryProtocol
from repositories.rabbit import RabbitRepository
from repositories.chat import ChatRepositoryProtocol
from repositories.chat import ChatRepository


class ChatServiceProtocol(Protocol):
	"""
	"""

	def __init__(
			self: Self,
			redis_repository: RedisRepositoryProtocol,
			rabbit_repository: RabbitRepositoryProtocol,
			chat_repository: ChatRepositoryProtocol,
	) -> None:	...

	async def send_chat_stats(
			self: Self,
			payload: GenerateStatsSchema,
	) -> None:	...


class ChatServiceImpl:
	"""
	"""

	def __init__(
			self: Self,
			redis_repository: RedisRepositoryProtocol,
			rabbit_repository: RabbitRepositoryProtocol,
			chat_repository: ChatRepositoryProtocol,
	) -> None:
		self.redis_repository = redis_repository
		self.rabbit_repository = rabbit_repository
		self.chat_repository = chat_repository

	async def send_chat_stats(
			self: Self,
			payload: GenerateStatsSchema,
	) -> None:
		"""
		"""
		cache = await self.redis_repository.get_chat_stats(
			chat_tg_id=payload.chat_tg_id,
		)
		if not cache:
			return await self.rabbit_repository.generate_chat_stats(
				payload=payload,
			)

		await self.chat_repository.send_chat_stats(
			payload=cache,
		)


def get_chat_service() -> ChatServiceProtocol:
	"""
	"""
	return ChatServiceImpl(
		redis_repository=RedisRepository,
		rabbit_repository=RabbitRepository,
		chat_repository=ChatRepository,
	)


ChatService = get_chat_service()