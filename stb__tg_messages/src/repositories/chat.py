from typing import Protocol
from typing import Self

from stbcore.schemas.redis import ChatStatsCacheSchema

from repositories.minio import MinioRepository
from repositories.minio import MinioRepositoryProtocol
from repositories.aiogram import AiogramRepository
from repositories.aiogram import AiogramRepositoryProtocol


class ChatRepositoryProtocol(Protocol):
	"""
	"""

	def __init__(
			self: Self,
			minio_repository: MinioRepositoryProtocol,
			aiogram_repository: AiogramRepositoryProtocol,
	) -> None:	...

	async def send_chat_stats(
			self: Self,
			payload: ChatStatsCacheSchema,
	) -> None:	...


class ChatRepositoryImpl:
	"""
	"""

	def __init__(
			self: Self,
			minio_repository: MinioRepositoryProtocol,
			aiogram_repository: AiogramRepositoryProtocol,
	) -> None:
		self.minio_repository = minio_repository
		self.aiogram_repository = aiogram_repository

	async def send_chat_stats(
			self: Self,
			payload: ChatStatsCacheSchema,
	) -> None:
		"""
		"""
		file_object = self.minio_repository.read_chat_stats_file(
			filename=payload.minio_object_name,
		)
		await self.aiogram_repository.send_chat_stats(
			payload=payload,
			file_object=file_object,
		)


def get_chat_repository() -> ChatRepositoryProtocol:
	"""
	"""
	return ChatRepositoryImpl(
		minio_repository=MinioRepository,
		aiogram_repository=AiogramRepository,
	)


ChatRepository = get_chat_repository()