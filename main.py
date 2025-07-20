#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import logging
import sys

from src.app import bot, dp
from src.routes import routers
from src.infra.kafka import Kafka
from src.infra.postgres import Postgres
from src.infra.rabbit import Rabbit


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
