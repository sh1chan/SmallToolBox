from aiogram import Router
from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message

from src.repositories.chat import ChatRepository


chat_router = Router(name=__name__)
chat_router.message.filter(
	F.chat,
	F.chat.id != F.from_user.id,
)


@chat_router.message(Command("cStats"))
async def default_stats(message: Message):
	"""
	"""
	return await ChatRepository.send_chat_stats(
		message=message,
	)