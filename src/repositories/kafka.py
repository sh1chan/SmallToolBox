from typing import Protocol
from typing import Self

from stbcore.core.enums import KafkaTopicsEnum
from stbcore.schemas.kafka import MessageEventSchema
from stbcore.infra.kafka import Kafka


class KafkaRepositoryProtocol(Protocol):
	"""
	"""

	async def publish_event(self: Self, payload: MessageEventSchema): ...


class KafkaRepositoryImpl:
	"""
	"""

	async def publish_event(self: Self, payload: MessageEventSchema):
		await Kafka.broker.publish(
			message=payload,
			topic=KafkaTopicsEnum.STB_EVENTS,
		)


def get_kafka_repository() -> KafkaRepositoryProtocol:
	return KafkaRepositoryImpl()


KafkaRepository = get_kafka_repository()