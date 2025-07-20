from typing import Self

from faststream.rabbit import RabbitBroker


class Rabbit:
  broker: RabbitBroker | None = None

  @classmethod
  async def initialize(cls: Self) -> None:
    cls.broker = RabbitBroker(
      "amqp://user:password@localhost:5672/"
    )
    await cls.broker.connect()

  @classmethod
  async def terminate(cls: Self) -> None:
    cls.broker.stop()