import datetime
from typing import Protocol
from typing import Self

from stbcore.models.user import UserStats
from stbcore.schemas.rabbit import GenerateUserStatsInSchema
from stbcore.schemas.redis import	UserStatsCacheSchema

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


class UserStatsServiceProtocol(Protocol):
	def __init__(
			self: Self,
			redis_repository: RedisRepositoryProtocol,
			rabbit_repository: RabbitRepositoryProtocol,
			postgres_repository: PostgresRepositoryProtocol,
			minio_repository: MinioRepositoryProtocol,
			user_stats: MinioRepositoryProtocol,
	) -> None:	...
	def generate_cache_and_send(self: Self, payload: GenerateUserStatsInSchema) -> None:	...


class UserStatsServiceImpl:
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

	async def generate_cache_and_send(self: Self, payload: GenerateUserStatsInSchema) -> None:
		"""Generates caches and sends the user stats

		Steps
			- Postgres.load_user_messages()
			- Generate
			- Minio.upload
			- Postgres.update
			- Redis.cache
			- Rabbit.send
		"""
		now = datetime.datetime.now()
		hourly_stats_date = (
			now.date - now.timedelta(hours=1)
		).strftime(
			format="%Y-%m-%d %H"
		)

		hourly_user_stats: UserStats | None = await self.postgres_repository.read_hourly_user_stats(
			user_tg_id=payload.user_tg_id,
			hourly_stats_date=hourly_stats_date,
		)
		if hourly_user_stats:
			self.minio_repository.delete_user_stats_file(filename=hourly_user_stats.report_filepath)
			# await self.postgres_repository.delete_hourly_user_stats(user_stats_id=hourly_user_stats.id)

		filename = f"user_stats_{hourly_stats_date}.png"

		user_stats_file_as_bytes = self.user_stats_repository.generate(
			hourly_user_stats=hourly_user_stats,
		)

		MinioRepository.create_user_stats_file(
			filename=filename, file_as_bytes=user_stats_file_as_bytes,
		)
		PostgresRepository.update_user_stats_filename(
			user_stats_id=hourly_user_stats.id,
			filename=filename,
		)
		RedisRepository.create_user_stats_cache(
			payload=UserStatsCacheSchema(
				minio_object_name=filename,
			),
		)

		# Ping service `stb__tg_messages`
		await RabbitRepository.send_user_stats(
			payload=payload,
		)

		# else:
		# 	us = await us_crud.generate(session, user.id, date)
		# 	report_filepath = stats.default(us)
		# 	us.report_filepath = report_filepath
		# 	await session.commit()

		# await message.reply_photo(
		# 	input_file.FSInputFile(report_filepath)
		# )


def get_user_stats_service() -> UserStatsServiceProtocol:
	return UserStatsServiceImpl(
		redis_repository=RedisRepository,
		rabbit_repository=RabbitRepository,
		postgres_repository=PostgresRepository,
		minio_repository=MinioRepository,
		user_stats_repository=UserStatsRepository,
	)


UserStatsService = get_user_stats_service()