from typing import Protocol
from typing import Self

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
	def generate_cache_and_send(self: Self) -> None:	...


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

	def generate_cache_and_send(self: Self) -> None:
		"""Generates caches and sends the user stats

		Steps
			- Postgres.load_user_stats
			- Generate
			- Minio.upload
			- Postgres.update
			- Redis.cache
			- Rabbit.send
		"""


def get_user_stats_service() -> UserStatsServiceProtocol:
	return UserStatsServiceImpl(
		redis_repository=RedisRepository,
		rabbit_repository=RabbitRepository,
		postgres_repository=PostgresRepository,
		minio_repository=MinioRepository,
		user_stats_repository=UserStatsRepository,
	)


UserStatsService = get_user_stats_service()