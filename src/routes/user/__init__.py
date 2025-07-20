import datetime

from aiogram import Router
from aiogram.types import Message, input_file
from aiogram.filters import Command

from src.infra.postgres import Postgres

from . import template, stats, crud


router = Router(name=__name__)


@router.message(Command("uStats"))
async def default_stats(message: Message):
  user = message.from_user
  if not user:
    return await message.reply(template.USERS_ONLY_COMMAND)

  async with Postgres.session_maker() as session:
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
