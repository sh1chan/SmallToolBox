from typing import Protocol
from typing import Self

from stbcore.schemas.rabbit import GenerateUserStatsInSchema

from repositories.redis import RedisRepositoryProtocol
from repositories.redis import RedisRepository
from repositories.rabbit import RabbitRepositoryProtocol
from repositories.rabbit import RabbitRepository


class UserStatsServiceProtocol(Protocol):
	def __init__(
			self: Self,
			redis_repository: RedisRepositoryProtocol,
			rabbit_repository: RabbitRepositoryProtocol,
	):	...
	async def send_user_stats(self: Self, payload: GenerateUserStatsInSchema) -> None:	...


class UserStatsServiceImpl:
	def __init__(
			self: Self,
			redis_repository: RedisRepositoryProtocol,
			rabbit_repository: RabbitRepositoryProtocol,
	):
		self.redis_repository = redis_repository
		self.rabbit_repository = rabbit_repository

	async def send_user_stats(self: Self, payload: GenerateUserStatsInSchema) -> None:
		print(f"Trying to send a user stats for: {payload.user_tg_id=}")
		cache = await self.redis_repository.get_user_stats(user_tg_id=payload.user_tg_id)
		print(f'{cache=}')

		if not cache:
			await self.rabbit_repository.generate_user_stats(payload=payload.user_tg_id)
			return 


def get_user_stats_service() -> UserStatsServiceProtocol:
	return UserStatsServiceImpl(
		redis_repository=RedisRepository,
		rabbit_repository=RabbitRepository,
	)


UserStatsService = get_user_stats_service()