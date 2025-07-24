from typing import Protocol
from typing import Self

from aiogram.types import Message

from stbcore.schemas.rabbit import GenerateUserStatsInSchema

from repositories.rabbit import RabbitRepositoryProtocol


class UserRepositoryProtocol(Protocol):
	"""
	"""

	def __init__(
			self: Self,
			rabbit_repository: RabbitRepositoryProtocol
	):	...

	async def send_user_stats(self: Self, message: Message) -> None: ...


class UserRepositoryImpl:
	"""
	"""

	def __init__(
			self: Self,
			rabbit_repository: RabbitRepositoryProtocol,
	):
		self.rabbit_repository = rabbit_repository

	async def send_user_stats(self: Self, message: Message) -> None:
		"""Publishes a message to send a user stats from the cache
		"""
		await self.rabbit_repository.send_user_stats(
			payload=GenerateUserStatsInSchema(
				user_tg_id=message.from_user.id,
				message_tg_id=message.message_id,
			),
		)


def get_user_repository() -> UserRepositoryProtocol:
	return UserRepositoryImpl()


UserRepository = get_user_repository()