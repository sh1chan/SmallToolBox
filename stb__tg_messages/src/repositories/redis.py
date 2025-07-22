from typing import Protocol
from typing import Self
from enum import Enum

from pydantic import PositiveInt

from stbcore.infra.redis import Redis


class CacheNamesEnum(str, Enum):
	USER_STATS = "user_stats:{user_tg_id}"


class RedisRepositoryProtocol(Protocol):
	async def get_user_stats(self: Self, user_tg_id: PositiveInt) -> None:
		...


class RedisRespositoryImpl:

	async def get_user_stats(self: Self, user_tg_id: PositiveInt):
		# stats_image_location
		return await Redis.client.get(
			CacheNamesEnum.USER_STATS.format(user_tg_id=user_tg_id)
		)
		print("Ans:", ans)


RedisRepository = RedisRespositoryImpl()