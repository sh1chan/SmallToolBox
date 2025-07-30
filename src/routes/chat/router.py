import datetime

from aiogram import Router
from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import input_file

from stbcore.infra.postgres import Postgres

# from . import template, crud, stats
from src.repositories.chat import ChatRepository


chat_router = Router(name=__name__)
chat_router.message.filter(
	F.chat,
	F.chat.id != F.from_user.id,
)


# @router.message(Command("gRegister"))
# async def msg(message: Message, command: CommandObject):
#   if not command.args:
#     return await message.reply(
#       template.MISSING_GROUP_REGISTER_ARGUMENT
#     )

@chat_router.message(Command("cStats"))
async def default_stats(message: Message):
	"""
	"""
	return await ChatRepository.send_chat_stats(
		message=message,
	)

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
