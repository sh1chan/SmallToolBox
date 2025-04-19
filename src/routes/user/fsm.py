from aiogram import Bot, Dispatcher, F, Router, html

from aiogram.client.default import DefaultBotProperties

from aiogram.enums import ParseMode

from aiogram.filters import Command, CommandStart

from aiogram.fsm.context import FSMContext

from aiogram.fsm.state import State, StatesGroup

from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)


class Edit(StatesGroup):
    name = State()
    like_bots = State()
    language = State()
