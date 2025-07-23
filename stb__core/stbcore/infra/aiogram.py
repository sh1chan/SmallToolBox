from typing import Self

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from stbcore.core.config import settings


class Aiogram:
	bot: Bot | None = None

	@classmethod
	async def initialize(cls: Self) -> None:
		cls.bot = Bot(
			token=settings.tgbot.token,
			default=DefaultBotProperties(parse_mode=ParseMode.HTML)
		)

	@classmethod
	async def terminate(cls: Self) -> None:
		cls.bot.close()