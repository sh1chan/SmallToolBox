""" Apache Kafka Infra
"""


__all__ = (
	"Kafka",
)


from typing import Self

from faststream.kafka import KafkaBroker

from stbcore.core.config import settings


class Kafka:
	"""
	"""
	broker: KafkaBroker | None = None

	@classmethod
	async def initialize(cls: Self) -> None:
		"""
		"""
		cls.broker = KafkaBroker(bootstrap_servers=settings.kafka.bootstrap_servers)
		await cls.broker.connect(bootstrap_servers=settings.kafka.bootstrap_servers)

	@classmethod
	async def terminate(cls: Self) -> None:
		"""
		"""
		await cls.broker.stop()