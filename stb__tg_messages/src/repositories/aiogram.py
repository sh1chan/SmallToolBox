from typing import Protocol
from typing import Self

from aiogram.types import input_file

from stbcore.schemas.redis import	UserStatsCacheSchema
from stbcore.infra.aiogram import	Aiogram


__all__ = (
	"AiogramRepository",
	"AiogramRepositoryProtocol",
)


class AiogramRepositoryProtocol(Protocol):
	"""
	"""

	async def send_user_stats(
			self: Self,
			payload: UserStatsCacheSchema,
			file_object: bytes,
	) -> None:	...


class AiogramRepositoryImpl:
	"""
	"""

	async def send_user_stats(
			self: Self,
			payload: UserStatsCacheSchema,
			file_object: bytes,
	) -> None:
		await Aiogram.bot.send_photo(
			chat_id=payload.user_tg_id,
			photo=input_file.BufferedInputFile(
				file=file_object,
				filename=payload.minio_object_name,
			),
		)


def get_aiogram_repository() -> AiogramRepositoryProtocol:
	return AiogramRepositoryImpl()


AiogramRepository = get_aiogram_repository()