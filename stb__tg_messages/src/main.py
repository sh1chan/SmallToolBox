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
from stbcore.infra.minio import Minio
from stbcore.infra.aiogram import Aiogram

from services.user_stats import UserStatsService


async def initialize():
	# Async
	await Redis.initialize()
	await Redis.initialize_client()
	await Rabbit.initialize()
	await Rabbit.broker.start()
	await Aiogram.initialize()

	# Sync
	Minio.initialize()


async def terminate():
	# Async
	await Redis.terminate()
	await Rabbit.terminate()
	
	# Sync
	Minio.terminate()


async def main():
	app = FastStream(broker=Rabbit.broker)

	@app.broker.subscriber(RabbitRoutingKeysEnum.TG_MESSAGES__USER_STATS)
	async def send_user_stats(payload: GenerateUserStatsInSchema) -> None:
		"""Sending user stats from the cache
		"""
		return await UserStatsService.send_user_stats(payload=payload)

	await app.run()


if __name__ == "__main__":
	runner = asyncio.Runner()
	try:
		runner.run(initialize())
		runner.run(main())
	finally:
		runner.run(terminate())