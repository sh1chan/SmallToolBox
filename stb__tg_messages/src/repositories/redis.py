import json

from typing import Protocol
from typing import Self

from pydantic import PositiveInt
from pydantic import NegativeInt

from stbcore.core.enums import RedisCacheNamesEnum
from stbcore.core.utils import redis_stats_datetime
from stbcore.schemas.redis import UserStatsCacheSchema
from stbcore.schemas.redis import ChatStatsCacheSchema
from stbcore.infra.redis import Redis


__all__ = (
	"RedisRepository",
	"RedisRepositoryProtocol",
)


class RedisRepositoryProtocol(Protocol):
	"""
	"""

	async def get_user_stats(
			self: Self,
			user_tg_id: PositiveInt,
	) -> UserStatsCacheSchema | None:	...

	async def get_chat_stats(
			self: Self,
			chat_tg_id: NegativeInt,
	) -> ChatStatsCacheSchema | None:	...


class RedisRespositoryImpl:
	"""
	"""

	async def get_user_stats(
			self: Self,
			user_tg_id: PositiveInt,
	) -> UserStatsCacheSchema | None:
		"""
		"""
		data = await Redis.client.get(
			name=RedisCacheNamesEnum.USER_STATS.format(
				user_tg_id=user_tg_id,
				datetime=redis_stats_datetime(),
			)
		)
		if data:
			return UserStatsCacheSchema(**json.loads(data.decode()))

	async def get_chat_stats(
			self: Self,
			chat_tg_id: NegativeInt,
	) -> ChatStatsCacheSchema | None:
		"""
		"""
		data = await Redis.client.get(
			name=RedisCacheNamesEnum.CHAT_STATS.format(
				chat_tg_id=chat_tg_id,
				datetime=redis_stats_datetime(),
			),
		)
		if data:
			return ChatStatsCacheSchema(**json.loads(data.decode()))


RedisRepository = RedisRespositoryImpl()