""" Redis Infra
"""


__all__ = (
	"Redis",
)


from typing import Self

import redis
from faststream.redis import RedisBroker

from stbcore.core.config import settings


class Redis:
	"""
	"""
	broker: RedisBroker | None = None
	client: redis.Redis | None = None

	@classmethod
	async def initialize(cls: Self) -> None:
		"""
		"""
		cls.broker = RedisBroker(url=settings.redis.broker_url)

	@classmethod
	async def initialize_client(cls: Self) -> None:
		"""
		"""
		cls.client = await cls.broker.connect()

	@classmethod
	async def terminate(cls: Self) -> None:
		"""
		"""
		await cls.client.close()
		await cls.broker.stop()