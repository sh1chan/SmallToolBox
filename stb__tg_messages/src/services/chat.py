from typing import Protocol
from typing import Self


from repositories.redis import RedisRepositoryProtocol
from repositories.redis import RedisRepository
from repositories.rabbit import RabbitRepositoryProtocol
from repositories.rabbit import RabbitRepository


class ChatServiceProtocol(Protocol):
	"""
	"""

	def __init__(
			self: Self,
			redis_repository: RedisRepositoryProtocol,
			rabbit_repository: RabbitRepositoryProtocol,
	) -> None:	...



class ChatServiceImpl:
	"""
	"""

	def __init__(
			self: Self,
			redis_repository: RedisRepositoryProtocol,
			rabbit_repository: RabbitRepositoryProtocol,
	) -> None:
		self.redis_repository = redis_repository
		self.rabbit_repository = rabbit_repository



def get_chat_service() -> ChatServiceProtocol:
	"""
	"""
	return ChatServiceImpl(
		redis_repository=RedisRepository,
		rabbit_repository=RabbitRepository,
	)


ChatService = get_chat_service()