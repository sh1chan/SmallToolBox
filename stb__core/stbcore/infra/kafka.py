from typing import Self

from faststream.kafka import KafkaBroker

from stbcore.core.config import settings


class Kafka:
	broker: KafkaBroker | None = None

	@classmethod
	async def initialize(cls: Self) -> None:
		cls.broker = KafkaBroker(bootstrap_servers=settings.kafka_bootstrap_servers)
		await cls.broker.connect()

	@classmethod
	async def terminate(cls: Self) -> None:
		cls.broker.stop()