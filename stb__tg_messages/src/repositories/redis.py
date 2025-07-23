import json

from typing import Protocol
from typing import Self

from pydantic import PositiveInt

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
	async def get_user_stats(self: Self, user_tg_id: PositiveInt) -> UserStatsCacheSchema | None:
		...


class RedisRespositoryImpl:
	"""
	"""
	async def get_user_stats(self: Self, user_tg_id: PositiveInt) -> UserStatsCacheSchema | None:
		data = await Redis.client.get(
			RedisCacheNamesEnum.USER_STATS.format(
				user_tg_id=user_tg_id,
				datetime=redis_user_stats_datetime(),
			)
		)
		if data:
			return UserStatsCacheSchema(**json.loads(data.decode()))


RedisRepository = RedisRespositoryImpl()