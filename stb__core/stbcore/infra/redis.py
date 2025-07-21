from typing import Self

from faststream.redis import RedisBroker

from stbcore.core.config import settings


class Redis:
	broker: RedisBroker | None = None

	@classmethod
	async def initialize(cls: Self) -> None:
		cls.broker = RedisBroker(url=settings.redis.broker_url)

	@classmethod
	async def terminate(cls: Self) -> None:
		await cls.broker.stop()