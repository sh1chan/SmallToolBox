from typing import Protocol
from typing import Self

from stbcore.schemas.rabbit import GenerateStatsSchema
from stbcore.schemas.redis import ChatStatsCacheSchema

from repositories.redis import RedisRepositoryProtocol
from repositories.redis import RedisRepository
from repositories.rabbit import RabbitRepositoryProtocol
from repositories.rabbit import RabbitRepository
from repositories.postgres import PostgresRepositoryProtocol
from repositories.postgres import PostgresRepository
from repositories.minio import MinioRepositoryProtocol
from repositories.minio import MinioRepository
from repositories.chat_stats import ChatStatsRepositoryProtocol
from repositories.chat_stats import ChatStatsRepository


__all__ = (
	"ChatStatsService",
	"ChatStatsServiceProtocol",
)


class ChatStatsServiceProtocol(Protocol):
	"""
	"""

	def __init__(
			self: Self,
			redis_repository: RedisRepositoryProtocol,
			rabbit_repository: RabbitRepositoryProtocol,
			postgres_repository: PostgresRepositoryProtocol,
			minio_repository: MinioRepositoryProtocol,
			chat_stats_repository: ChatStatsRepositoryProtocol,
	) -> None:	...

	async def generate_cache_and_send(
			self: Self,
			payload: GenerateStatsSchema,
	) -> None:	...


class ChatStatsServiceImpl:
	"""
	"""

	def __init__(
			self: Self,
			redis_repository: RedisRepositoryProtocol,
			rabbit_repository: RabbitRepositoryProtocol,
			postgres_repository: PostgresRepositoryProtocol,
			minio_repository: MinioRepositoryProtocol,
			chat_stats_repository: ChatStatsRepositoryProtocol,
	) -> None:
		self.redis_repository = redis_repository
		self.rabbit_repository = rabbit_repository
		self.postgres_repository = postgres_repository
		self.minio_repository = minio_repository
		self.chat_stats_repository = chat_stats_repository

	async def generate_cache_and_send(
			self: Self,
			payload: GenerateStatsSchema,
	) -> None:
		""" Generates, Caches, and Sends the chat stats
		"""
		stats_date = payload.message_date.strftime("%Y-%m-%d")
		filename = f"user_stats_{stats_date}.png"

		chat_stats = await self.postgres_repository.read_chat_stats(
			chat_tg_id=payload.chat_tg_id,
			date=stats_date,
		)
		if chat_stats:
			self.minio_repository.delete_chat_stats_file(
				filename=chat_stats.report_filepath,
			)

		chat_stats = await self.postgres_repository.create_chat_stats(
			chat_tg_id=payload.chat_tg_id,
			date=stats_date,
			chat_stats=chat_stats,
			filename=filename,
		)

		chat_stats_file_as_bytes = self.chat_stats_repository.generate(
			chat_stats=chat_stats,
		)

		self.minio_repository.create_chat_stats_file(
			filename=filename,
			file_as_bytes=chat_stats_file_as_bytes,
		)

		await self.redis_repository.create_chat_stats_cache(
			payload=ChatStatsCacheSchema(
				chat_tg_id=payload.chat_tg_id,
				minio_object_name=filename,
			),
		)

		await self.rabbit_repository.send_chat_stats(
			payload=payload,
		)


def get_chat_stats_service() -> ChatStatsServiceProtocol:
	"""
	"""
	return ChatStatsServiceImpl(
	 	redis_repository=RedisRepository,
		rabbit_repository=RabbitRepository,
		postgres_repository=PostgresRepository,
		minio_repository=MinioRepository,
		chat_stats_repository=ChatStatsRepository,
	)


ChatStatsService = get_chat_stats_service()