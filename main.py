#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import logging
import sys

from src.app import bot, dp
from src.routes import routers
from src.infra.kafka import Kafka
from src.infra.postgres import Postgres


async def initialize():
	dp.include_routers(
		*routers
	)
	await Postgres.initialize()
	await Kafka.initialize()


async def terminate():
	await Postgres.terminate()
	await Kafka.terminate()


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
