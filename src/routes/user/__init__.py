import datetime

from aiogram import Router
from aiogram.types import Message, input_file
from aiogram.filters import Command

from src.sql import db

from . import template, stats, crud


router = Router(name=__name__)


@router.message(Command("uStats"))
async def default_stats(message: Message):
  user = message.from_user
  if not user:
    return await message.reply(template.USERS_ONLY_COMMAND)

  session_maker = await db.get_session()

  async with session_maker() as session:
    date = (
        message.date - datetime.timedelta(hours=1)
    ).strftime("%Y-%m-%d %H")
    us_crud = crud.UserStats()
    us = await us_crud.get(session, user.id, date)
    if us:
      report_filepath = us.report_filepath
    else:
      us = await us_crud.generate(session, user.id, date)
      if us is None:
        return await message.reply(template.NO_STATS_TO_GENERATE)
      report_filepath = stats.default(us)
      us.report_filepath = report_filepath
      await session.commit()
    await message.reply_photo(
      input_file.FSInputFile(report_filepath)
    )


@router.message(Command("uProgressBar"))
async def default_stats(message: Message):
  user = message.from_user
  if not user:
    return await message.reply(template.USERS_ONLY_COMMAND)
  # TODO
  # - get all progress / limit 5
  # - add Pagination buttons
  # - add Action buttons

  buttons = []

  from aiogram.types import ReplyKeyboardMarkup
  from aiogram.types.keyboard_button import KeyboardButton

  session_maker = await db.get_session()

  async with session_maker() as session:
    for pb in await crud.ProgressBar.get(
      session=session, user_id=user.id,
    ):
      buttons.append(
        KeyboardButton(text=pb.name)
      )

  await message.reply(
    text="EE",
    reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='fefef')]])
  )