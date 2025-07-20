#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import logging
import sys

from src.app import bot, dp
from src.sql import db
from src.routes import routers


async def initialize():
  dp.include_routers(
    *routers
  )
  await db.initialize()


async def terminate():
  await db.terminate()


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
