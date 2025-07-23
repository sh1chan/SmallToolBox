from typing import Protocol
from typing import Self

from stbcore.core.enums import RedisCacheNamesEnum
from stbcore.core.utils import redis_user_stats_datetime
from stbcore.schemas.redis import UserStatsCacheSchema
from stbcore.infra.redis import Redis


__all__ = (
	"RedisRepository",
	"RedisRepositoryProtocol",
)


class RedisRepositoryProtocol(Protocol):
	"""
	"""

	async def create_user_stats_cache(self: Self, payload: UserStatsCacheSchema) -> None:	...


class RedisRepositoryImpl:
	"""
	"""

	async def create_user_stats_cache(self: Self, payload: UserStatsCacheSchema) -> None:
		# XXX (ames0k0): 10 minutes cache
		await Redis.client.set(
			name=RedisCacheNamesEnum.USER_STATS.format(
				user_tg_id=payload.user_tg_id,
				datetime=redis_user_stats_datetime(),
			),
			value=payload.model_dump_json(),
			ex=10*60
		)


RedisRepository = RedisRepositoryImpl()