from typing import Protocol
from typing import Self

from stbcore.core.enums import RabbitRoutingKeysEnum
from stbcore.schemas.rabbit import GenerateUserStatsInSchema
from stbcore.infra.rabbit import Rabbit


__all__ = (
	"RabbitRepository",
	"RabbitRepositoryProtocol",
)


class RabbitRepositoryProtocol(Protocol):
	"""
	"""

	async def send_user_stats(self: Self, payload: GenerateUserStatsInSchema) -> None:	...


class RabbitRepositoryImpl:
	"""
	"""

	async def send_user_stats(self: Self, payload: GenerateUserStatsInSchema) -> None:
		"""Publishes a message to send a user stats from the cache
		"""
		await Rabbit.broker.publish(
			message=payload,
			routing_key=RabbitRoutingKeysEnum.TG_MESSAGES__USER_STATS,
		)


RabbitRepository = RabbitRepositoryImpl()