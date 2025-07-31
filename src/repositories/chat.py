from typing import Protocol
from typing import Self

from aiogram.types import Message

from stbcore.schemas.rabbit import GenerateStatsSchema

from .rabbit import RabbitRepository
from .rabbit import RabbitRepositoryProtocol


class ChatRepositoryProtocol(Protocol):
	"""
	"""

	def __init__(
			self: Self,
			rabbit_repository: RabbitRepositoryProtocol,
	) -> None:	...

	async def send_chat_stats(
			self: Self,
			message: Message,
	) -> None:	...


class ChatRepositoryImpl:
	"""
	"""

	def __init__(
			self: Self,
			rabbit_repository: RabbitRepositoryProtocol,
	) -> None:
		self.rabbit_repository = rabbit_repository

	async def send_chat_stats(
			self: Self,
			message: Message,
	) -> None:
		"""
		"""
		await self.rabbit_repository.send_chat_stats(
			payload=GenerateStatsSchema(
				chat_tg_id=message.chat.id,
				user_tg_id=message.from_user.id,
				message_tg_id=message.message_id,
				message_date=message.date,
			),
		)


def get_chat_repository() -> ChatRepositoryProtocol:
	"""
	"""
	return ChatRepositoryImpl(
		rabbit_repository=RabbitRepository,
	)


ChatRepository = get_chat_repository()