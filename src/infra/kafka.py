from faststream.kafka import KafkaBroker

from src import config


class Kafka:
	broker: KafkaBroker | None = None

	@classmethod
	async def initialize(cls):
		cls.broker = KafkaBroker(
			bootstrap_servers=config.env["KAFKA_BOOTSTRAP_SERVERS"]
		)

	@classmethod
	async def terminate(cls):
		await cls.broker.stop()