import asyncio
import logging
import sys
import os

if not os.environ.get("IS_IN_PRODUCTION_MODE"):
	from dotenv import find_dotenv, load_dotenv
	load_dotenv(find_dotenv())

from aiogram import Dispatcher

from stbcore.infra.kafka import Kafka
from stbcore.infra.rabbit import Rabbit
from stbcore.infra.aiogram import Aiogram

from routes import routers


async def initialize():
	"""
	"""
	# Async
	await Kafka.initialize()
	await Rabbit.initialize()
	await Aiogram.initialize()

	# Routers
	dispatcher.include_routers(
		*routers
	)


async def terminate():
	"""
	"""
	# Async
	await Kafka.terminate()
	await Rabbit.terminate()


async def main():
	"""
	"""
	await dispatcher.start_polling(Aiogram.bot)


if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO, stream=sys.stdout)

	dispatcher = Dispatcher()
	runner = asyncio.Runner()

	try:
		runner.run(initialize())
		runner.run(main())
	finally:
		runner.run(terminate())