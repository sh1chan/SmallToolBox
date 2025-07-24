from aiogram import Router, html, types
from aiogram.filters import CommandStart

from src.repositories.root import RootRepository
from . import template


router = Router(name=__name__)


@router.message(CommandStart())
async def command_start_handler(message: types.Message):
	user = message.from_user
	if not user:
		return await message.answer(template.NOT_IMPLEMENTED)

	await message.answer(
		template.WELCOME.format(
			NAME=f"{html.bold(message.from_user.full_name)}"
		)
	)


async def dump_private_chat_message(message: types.Message):
	await message.reply_document(
		document=types.BufferedInputFile(
			file=message.model_dump_json(
				exclude_unset=True,
				exclude_none=True,
				exclude_defaults=True,
				indent=2,
			).encode(),
			filename=f"{message.message_id}.json"
		),
		caption="<blockquote>\nexclude_unset=True\nexclude_none=True\nexclude_defaults=True</blockquote>",
	)


@router.message()
async def any_message(message: types.Message):
	"""Any Messages

	User
		- check user_message_settings
			- save_messages
			- save_stats
	Chat
		- check chat_message_settings
			- save_stats
	"""
	if message.chat.type == "private":
		return await dump_private_chat_message(message=message)

	await RootRepository.register_message(
		message=message,
	)