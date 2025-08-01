""" RabbitMQ Infra
"""


__all__ = (
	"Rabbit",
)


from typing import Self

from faststream.rabbit import RabbitBroker

from stbcore.core.config import settings


class Rabbit:
	"""
	"""
	broker: RabbitBroker | None = None

	@classmethod
	async def initialize(cls: Self) -> None:
		"""
		"""
		cls.broker = RabbitBroker(url=settings.rabbit.broker_url)
		await cls.broker.connect()

	@classmethod
	async def terminate(cls: Self) -> None:
		"""
		"""
		await cls.broker.stop()