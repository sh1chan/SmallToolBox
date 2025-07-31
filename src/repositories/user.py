from typing import Protocol
from typing import Self

from aiogram.types import Message

from stbcore.schemas.rabbit import GenerateStatsSchema

from .rabbit import RabbitRepository
from .rabbit import RabbitRepositoryProtocol


class UserRepositoryProtocol(Protocol):
	"""
	"""

	def __init__(
			self: Self,
			rabbit_repository: RabbitRepositoryProtocol
	) -> None:	...

	async def send_user_stats(
			self: Self,
			message: Message,
	) -> None:	...


class UserRepositoryImpl:
	"""
	"""

	def __init__(
			self: Self,
			rabbit_repository: RabbitRepositoryProtocol,
	) -> None:
		self.rabbit_repository = rabbit_repository

	async def send_user_stats(self: Self, message: Message) -> None:
		"""Publishes a message to send a user stats from the cache
		"""
		await self.rabbit_repository.send_user_stats(
			payload=GenerateStatsSchema(
				chat_tg_id=message.chat.id,
				user_tg_id=message.from_user.id,
				message_tg_id=message.message_id,
				message_date=message.date,
			),
		)


def get_user_repository() -> UserRepositoryProtocol:
	"""
	"""
	return UserRepositoryImpl(
		rabbit_repository=RabbitRepository,
	)


UserRepository = get_user_repository()