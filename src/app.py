from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src import config

bot = Bot(
    token=config.env["TOKEN"],
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)

dp = Dispatcher()
