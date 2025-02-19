import datetime

from aiogram import Router, F, types, filters
from aiogram.types.keyboard_button import KeyboardButton

from src.core import const
from src.sql import db

from . import template, stats, crud


router = Router(name=__name__)


@router.message(filters.Command("uStats"))
async def default_stats(message: types.Message):
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
      types.input_file.FSInputFile(report_filepath)
    )


@router.callback_query(F.data == "ProgressBar:Add")
async def cal(query: types.CallbackQuery):
  print('Add')


@router.callback_query(F.data.startswith("ProgressBar:Edit:"))
async def cal(query: types.CallbackQuery):
  print('Edit')


@router.callback_query(F.data.startswith("ProgressBar:SwapStatus:"))
async def cal(query: types.CallbackQuery):
  print('Swap')


@router.message(filters.Command("uProgressBar"))
async def default_stats(message: types.Message):
  user = message.from_user
  if not user:
    return await message.reply(template.USERS_ONLY_COMMAND)
  # TODO
  # - get all progress / limit 5
  # - add Pagination buttons
  # - add Action buttons

  buttons = []

  session_maker = await db.get_session()

  async with session_maker() as session:
    for pb in await crud.ProgressBar.get(
      session=session, user_id=user.id,
    ):
      buttons.append(
        [
          types.inline_keyboard_button.InlineKeyboardButton(
            text=const.EmojiSet.ACTIVE \
              if pb.is_active else const.EmojiSet.DISABLED,
            callback_data=f'ProgressBar:SwapStatus:{pb.id}',
          ),
          types.inline_keyboard_button.InlineKeyboardButton(
            text=pb.name,
            callback_data=f'ProgressBar:Edit:{pb.id}',
          )
        ]
      )

  # TODO: pagination
  buttons.append(
    [
      types.inline_keyboard_button.InlineKeyboardButton(
        text=const.EmojiSet.PLUS,
        callback_data="ProgressBar:Add"
      ),
    ]
  )

  await message.reply(
    text="ProgressBar List...",
    reply_markup=types.inline_keyboard_markup.InlineKeyboardMarkup(
      inline_keyboard=buttons,
    ),
  )
