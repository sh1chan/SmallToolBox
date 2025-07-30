from typing import Protocol
from typing import Self

from stbcore.schemas.redis import UserStatsCacheSchema

from repositories.minio import MinioRepository
from repositories.minio import MinioRepositoryProtocol
from repositories.aiogram import AiogramRepository
from repositories.aiogram import AiogramRepositoryProtocol


__all__ = (
	"UserStatsRepository",
	"UserStatsRepositoryProtocol",
)


class UserStatsRepositoryProtocol(Protocol):
	"""
	"""

	def __init__(
			self: Self,
			aiogram_repository: AiogramRepositoryProtocol,
			minio_repository: MinioRepositoryProtocol,
	) -> None:	...

	async def send_user_stats(
			self: Self,
			payload: UserStatsCacheSchema,
	) -> None:	...


class UserStatsRespositoryImpl:
	"""
	"""

	def __init__(
			self: Self,
			aiogram_repository: AiogramRepositoryProtocol,
			minio_repository: MinioRepositoryProtocol,
	) -> None:
		self.aiogram_repository = aiogram_repository
		self.minio_repository = minio_repository

	async def send_user_stats(
			self: Self,
			payload: UserStatsCacheSchema,
	) -> None:
		"""
		"""
		file_object = self.minio_repository.read_user_stats_file(
			filename=payload.minio_object_name,
		)
		await self.aiogram_repository.send_user_stats(
			payload=payload,
			file_object=file_object,
		)


def get_user_stats_repository() -> UserStatsRepositoryProtocol:
	"""
	"""
	return UserStatsRespositoryImpl(
		aiogram_repository=AiogramRepository,
		minio_repository=MinioRepository,
	)


UserStatsRepository = get_user_stats_repository()