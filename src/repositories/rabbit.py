""" Rabbit Infra Repository
"""


__all__ = (
	"RabbitRepository",
	"RabbitRepositoryProtocol",
)


from typing import Protocol
from typing import Self

from stbcore.core.enums import RabbitRoutingKeysEnum
from stbcore.infra.rabbit import Rabbit

from stbcore.schemas.rabbit import GenerateStatsSchema


class RabbitRepositoryProtocol(Protocol):
	"""
	"""

	async def send_user_stats(
			self: Self,
			payload: GenerateStatsSchema,
	) -> None:	...

	async def send_chat_stats(
			self: Self,
			payload: GenerateStatsSchema,
	) -> None:	...


class RabbitRepositoryImpl:
	"""
	"""

	async def send_user_stats(
			self: Self,
			payload: GenerateStatsSchema,
	) -> None:
		""" Publishes a message to send a user stats from the cache
		"""
		await Rabbit.broker.publish(
			message=payload,
			routing_key=RabbitRoutingKeysEnum.TG_MESSAGES__USER_STATS,
		)

	async def send_chat_stats(
			self: Self,
			payload: GenerateStatsSchema,
	) -> None:
		"""
		"""
		await Rabbit.broker.publish(
			message=payload,
			routing_key=RabbitRoutingKeysEnum.TG_MESSAGES__CHAT_STATS,
		)


def get_rabbit_repository() -> RabbitRepositoryProtocol:
	"""
	"""
	return RabbitRepositoryImpl()


RabbitRepository = get_rabbit_repository()