from typing import Protocol
from typing import Self

from stbcore.core.enums import RabbitRoutingKeysEnum
from stbcore.infra.rabbit import Rabbit
from stbcore.schemas.rabbit import GenerateStatsSchema


__all__ = (
	"RabbitRepository",
	"RabbitRepositoryProtocol",
)


class RabbitRepositoryProtocol(Protocol):
	"""
	"""

	async def generagte_user_stats(
			self: Self,
			payload: GenerateStatsSchema,
	) -> None:	...

	async def generagte_chat_stats(
			self: Self,
			payload: GenerateStatsSchema,
	) -> None:	...


class RabbitRepositoryImpl:
	"""
	"""

	async def generate_user_stats(
			self: Self,
			payload: GenerateStatsSchema,
	) -> None:
		"""Publishes a message to send a user stats from the cache
		"""
		await Rabbit.broker.publish(
			message=payload,
			routing_key=RabbitRoutingKeysEnum.STATS_GENERATOR__USER_STATS,
		)

	async def generate_chat_stats(
			self: Self,
			payload: GenerateStatsSchema,
	) -> None:
		"""
		"""
		await Rabbit.broker.publish(
			message=payload,
			routing_key=RabbitRoutingKeysEnum.STATS_GENERATOR__CHAT_STATS,
		)


def get_rabbit_repository() -> RabbitRepositoryProtocol:
	"""
	"""
	return RabbitRepositoryImpl()


RabbitRepository = get_rabbit_repository()