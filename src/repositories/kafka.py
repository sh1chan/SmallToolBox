""" Kafka Infra Repository
"""


__all__ = (
	"KafkaRepository",
	"KafkaRepositoryProtocol",
)


from typing import Protocol
from typing import Self

from stbcore.core.enums import KafkaTopicsEnum
from stbcore.schemas.kafka import TelegramMessageEventSchema
from stbcore.infra.kafka import Kafka


class KafkaRepositoryProtocol(Protocol):
	"""
	"""

	async def publish_event(
			self: Self,
			payload: TelegramMessageEventSchema,
	) -> None:	...


class KafkaRepositoryImpl:
	"""
	"""

	async def publish_event(
			self: Self,
			payload: TelegramMessageEventSchema,
	) -> None:
		"""
		"""
		await Kafka.broker.publish(
			message=payload,
			topic=KafkaTopicsEnum.stb_events,
		)


def get_kafka_repository() -> KafkaRepositoryProtocol:
	"""
	"""
	return KafkaRepositoryImpl()


KafkaRepository = get_kafka_repository()