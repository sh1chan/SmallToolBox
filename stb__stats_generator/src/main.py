import os
import asyncio

if not os.environ.get("IS_IN_PRODUCTION_MODE"):
	from dotenv import find_dotenv, load_dotenv
	load_dotenv(find_dotenv())

from faststream import FastStream

from stbcore.core.enums import RabbitRoutingKeysEnum
from stbcore.schemas.rabbit import GenerateUserStatsInSchema
from stbcore.infra.redis import Redis
from stbcore.infra.rabbit import Rabbit
from stbcore.infra.postgres import Postgres
from stbcore.infra.minio import Minio

from services.user_stats import UserStatsService


async def initialize():
	# Async
	await Redis.initialize()
	await Redis.initialize_client()
	await Rabbit.initialize()
	await Rabbit.broker.start()
	await Postgres.initialize()

	# Sync
	Minio.initialize()


async def terminate():
	# Async
	await Redis.terminate()
	await Rabbit.terminate()
	await Postgres.terminate()

	# Sync
	Minio.terminate()


async def main():
	app = FastStream(broker=Rabbit.broker)

	@app.broker.subscriber(RabbitRoutingKeysEnum.STATS_GENERATOR__USER_STATS)
	async def generate_user_stats(payload: GenerateUserStatsInSchema) -> None:
		"""Generates user stats, caches and sends
		"""
		return await UserStatsService.generate_cache_and_send(
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