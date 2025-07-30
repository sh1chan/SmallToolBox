from typing import Protocol
from typing import Self

from stbcore.schemas.rabbit import GenerateStatsSchema

from repositories.redis import RedisRepositoryProtocol
from repositories.redis import RedisRepository
from repositories.rabbit import RabbitRepositoryProtocol
from repositories.rabbit import RabbitRepository
from repositories.user_stats import UserStatsRepository
from repositories.user_stats import UserStatsRepositoryProtocol


class UserStatsServiceProtocol(Protocol):
	def __init__(
			self: Self,
			redis_repository: RedisRepositoryProtocol,
			rabbit_repository: RabbitRepositoryProtocol,
			user_stats_repository: UserStatsRepositoryProtocol,
	):	...
	async def send_user_stats(self: Self, payload: GenerateStatsSchema) -> None:	...


class UserStatsServiceImpl:
	def __init__(
			self: Self,
			redis_repository: RedisRepositoryProtocol,
			rabbit_repository: RabbitRepositoryProtocol,
			user_stats_repository: UserStatsRepositoryProtocol,
	):
		self.redis_repository = redis_repository
		self.rabbit_repository = rabbit_repository
		self.user_stats_repository = user_stats_repository

	async def send_user_stats(self: Self, payload: GenerateStatsSchema) -> None:
		cache = await self.redis_repository.get_user_stats(user_tg_id=payload.user_tg_id)

		if not cache:
			await self.rabbit_repository.generate_user_stats(payload=payload)
			return 

		await self.user_stats_repository.send_user_stats(
			payload=cache,
		)


def get_user_stats_service() -> UserStatsServiceProtocol:
	return UserStatsServiceImpl(
		redis_repository=RedisRepository,
		rabbit_repository=RabbitRepository,
		user_stats_repository=UserStatsRepository,
	)


UserStatsService = get_user_stats_service()