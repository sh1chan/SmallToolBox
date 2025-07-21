#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import logging
import sys
import os

if not os.environ.get("IS_IN_PRODUCTION_MODE"):
	from dotenv import find_dotenv, load_dotenv
	load_dotenv(find_dotenv())

from stbcore.infra.kafka import Kafka
from stbcore.infra.postgres import Postgres
from stbcore.infra.rabbit import Rabbit

from src.app import bot, dp
from src.routes import routers


async def initialize():
	await Kafka.initialize()
	await Rabbit.initialize()
	await Postgres.initialize()

	dp.include_routers(
		*routers
	)


async def terminate():
	await Kafka.terminate()
	await Rabbit.terminate()
	await Postgres.terminate()


async def main():
	await dp.start_polling(bot)


if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO, stream=sys.stdout)

	runner = asyncio.Runner()

	try:
		runner.run(initialize())
		runner.run(main())
	finally:
		runner.run(terminate())
