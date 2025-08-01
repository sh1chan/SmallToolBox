import datetime
from typing import Protocol
from typing import Self

from stbcore.schemas.rabbit import GenerateStatsSchema
from stbcore.schemas.redis import UserStatsCacheSchema

from repositories.redis import RedisRepositoryProtocol
from repositories.redis import RedisRepository
from repositories.rabbit import RabbitRepositoryProtocol
from repositories.rabbit import RabbitRepository
from repositories.postgres import PostgresRepositoryProtocol
from repositories.postgres import PostgresRepository
from repositories.minio import MinioRepositoryProtocol
from repositories.minio import MinioRepository
from repositories.user_stats import UserStatsRepository
from repositories.user_stats import UserStatsRepositoryProtocol


__all__ = (
	"UserStatsService",
	"UserStatsServiceProtocol",
)


class UserStatsServiceProtocol(Protocol):
	"""
	"""

	def __init__(
			self: Self,
			redis_repository: RedisRepositoryProtocol,
			rabbit_repository: RabbitRepositoryProtocol,
			postgres_repository: PostgresRepositoryProtocol,
			minio_repository: MinioRepositoryProtocol,
			user_stats: MinioRepositoryProtocol,
	) -> None:	...

	async def generate_cache_and_send(
			self: Self,
			payload: GenerateStatsSchema,
	) -> None:	...


class UserStatsServiceImpl:
	"""
	"""

	def __init__(
			self: Self,
			redis_repository: RedisRepositoryProtocol,
			rabbit_repository: RabbitRepositoryProtocol,
			postgres_repository: PostgresRepositoryProtocol,
			minio_repository: MinioRepositoryProtocol,
			user_stats_repository: UserStatsRepositoryProtocol,
	) -> None:
		self.redis_repository = redis_repository
		self.rabbit_repository = rabbit_repository
		self.postgres_repository = postgres_repository
		self.minio_repository = minio_repository
		self.user_stats_repository = user_stats_repository

	async def generate_cache_and_send(
			self: Self,
			payload: GenerateStatsSchema,
	) -> None:
		""" Generates, Caches and Sends the user stats

		Steps
			- Postgres.load_user_messages()
			- Generate
			- Minio.upload
			- Postgres.update
			- Redis.cache
			- Rabbit.send

		Read UserStats
		Read MessageStats
		Calculate
			-> Create / Update UserStats
		Generate
		"""
		stats_date = payload.message_date.strftime("%Y-%m-%d")
		filename = f"user_stats_{stats_date}.png"

		user_stats = await self.postgres_repository.read_user_stats(
			user_tg_id=payload.user_tg_id,
			date=stats_date,
		)
		if user_stats:
			self.minio_repository.delete_user_stats_file(
				filename=user_stats.report_filepath,
			)

		user_stats = await self.postgres_repository.create_user_stats(
			user_tg_id=payload.user_tg_id,
			date=stats_date,
			user_stats=user_stats,
			filename=filename,
		)

		user_stats_file_as_bytes = self.user_stats_repository.generate(
			user_stats=user_stats,
		)

		self.minio_repository.create_user_stats_file(
			filename=filename,
			file_as_bytes=user_stats_file_as_bytes,
		)

		await self.redis_repository.create_user_stats_cache(
			payload=UserStatsCacheSchema(
				user_tg_id=payload.user_tg_id,
				minio_object_name=filename,
			),
		)

		# Ping service `stb__tg_messages`
		await self.rabbit_repository.send_user_stats(
			payload=payload,
		)


def get_user_stats_service() -> UserStatsServiceProtocol:
	"""
	"""
	return UserStatsServiceImpl(
		redis_repository=RedisRepository,
		rabbit_repository=RabbitRepository,
		postgres_repository=PostgresRepository,
		minio_repository=MinioRepository,
		user_stats_repository=UserStatsRepository,
	)


UserStatsService = get_user_stats_service()