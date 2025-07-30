from typing import Protocol
from typing import Self

from stbcore.core.enums import RabbitRoutingKeysEnum
from stbcore.infra.rabbit import Rabbit

from stbcore.schemas.rabbit import GenerateUserStatsInSchema


class RabbitRepositoryProtocol(Protocol):
	"""
	"""

	async def send_user_stats(
			self: Self,
			payload: GenerateUserStatsInSchema,
	) -> None:	...

	async def send_chat_stats(
			self: Self,
			payload: GenerateUserStatsInSchema,
	) -> None:	...


class RabbitRepositoryImpl:
	"""
	"""

	async def send_user_stats(
			self: Self,
			payload: GenerateUserStatsInSchema,
	) -> None:
		"""Publishes a message to send a user stats from the cache
		"""
		await Rabbit.broker.publish(
			message=payload,
			routing_key=RabbitRoutingKeysEnum.TG_MESSAGES__USER_STATS,
		)

	async def send_chat_stats(
			self: Self,
			payload: GenerateUserStatsInSchema,
	) -> None:
		await Rabbit.broker.publish(
			message=payload,
			routing_key=RabbitRoutingKeysEnum.TG_MESSAGES__CHAT_STATS,
		)


RabbitRepository = RabbitRepositoryImpl()