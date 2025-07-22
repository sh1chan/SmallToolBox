import json
from typing import Protocol
from typing import Self

from aiogram.types import Message

from stbcore.infra.rabbit import Rabbit


class RabbitRepositoryProtocol(Protocol):
  async def send_user_stats(self: Self, message: Message) -> None: ...


class RabbitRepositoryImpl:
  """
  """

  async def send_user_stats(self: Self, message: Message) -> None:
    """Publishes a message to send a user stats from the cache
    """
    await Rabbit.broker.publish(
      message=json.dumps({
        "user_tg_id": message.from_user.id,
      }),
      routing_key="user_stats",
    )


RabbitRepository = RabbitRepositoryImpl()