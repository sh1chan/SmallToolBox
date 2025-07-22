import datetime

from aiogram import Router
from aiogram import F
from aiogram.types import Message
from aiogram.types import input_file
from aiogram.filters import Command

from stbcore.infra.postgres import Postgres

from src.repositories.rabbit import RabbitRepository
from . import template, stats, crud


router = Router(name=__name__)
router.message.filter(F.from_user)


@router.message(Command("uStats"))
async def default_stats(message: Message):
	return await RabbitRepository.send_user_stats(
		message=message,
	)

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
