import datetime

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, input_file

from stbcore.infra.postgres import Postgres

from . import template, crud, stats


router = Router(name=__name__)


# @router.message(Command("gRegister"))
# async def msg(message: Message, command: CommandObject):
#   if not command.args:
#     return await message.reply(
#       template.MISSING_GROUP_REGISTER_ARGUMENT
#     )

@router.message(Command("cStats"))
async def default_stats(message: Message):
	chat = message.chat
	if not chat:
		return await message.reply(template.CHAT_ONLY_COMMAND)
	if message.from_user and message.from_user.id == chat.id:
		return await message.reply(template.CHAT_ONLY_COMMAND)

	async with Postgres.session_maker() as session:
		date = (
				message.date - datetime.timedelta(hours=1)
		).strftime("%Y-%m-%d %H")
		us_crud = crud.UserStats()
		us = await us_crud.get(session, chat.id, date)
		if us:
			report_filepath = us.report_filepath
		else:
			us = await us_crud.generate(session, chat.id, date)
			if us is None:
				return await message.reply(template.NO_STATS_TO_GENERATE)
			report_filepath = stats.default(us)
			us.report_filepath = report_filepath
			await session.commit()
		await message.reply_photo(
			input_file.FSInputFile(report_filepath)
		)
