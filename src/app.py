from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from stbcore.core.config import settings

bot = Bot(
	token=settings.tgbot.token,
	default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()