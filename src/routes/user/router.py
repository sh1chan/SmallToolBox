from aiogram import Router
from aiogram import F
from aiogram.types import Message
from aiogram.filters import Command

from src.repositories.user import UserRepository


user_router = Router(name=__name__)
user_router.message.filter(F.from_user)


@user_router.message(Command("uStats"))
async def user_stats(message: Message):
	"""
	"""
	await UserRepository.send_user_stats(
		message=message,
	)