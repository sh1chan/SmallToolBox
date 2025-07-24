import os
import asyncio

if not os.environ.get("IS_IN_PRODUCTION_MODE"):
	from dotenv import find_dotenv, load_dotenv
	load_dotenv(find_dotenv())

from faststream import FastStream

from stbcore.core.enums import KafkaTopicsEnum
from stbcore.schemas.kafka import MessageEventSchema
from stbcore.infra.kafka import Kafka
from stbcore.infra.postgres import Postgres

from services.events_analyzer import EventsAnalyzerService


async def initialize():
	"""
	"""
	await Kafka.initialize()
	await Postgres.initialize()


async def terminate():
	"""
	"""
	await Kafka.initialize()
	await Postgres.initialize()


async def main():
	"""
	"""
	app = FastStream(broker=Kafka.broker)

	@app.broker.subscriber(KafkaTopicsEnum.STB_EVENTS)
	async def message_events_analyzer(payload: MessageEventSchema) -> None:
		"""Analyzes the message events
		"""
		return await EventsAnalyzerService.message_events_analyzer(
			payload=payload,
		)

	await app.run()


if __name__ == "__main__":
	runner = asyncio.Runner()
	try:
		runner.run(initialize())
		runner.run(main())
	finally:
		runner.run(terminate())