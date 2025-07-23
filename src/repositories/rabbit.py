from typing import Protocol
from typing import Self

from aiogram.types import Message

from stbcore.core.enums import RabbitRoutingKeysEnum
from stbcore.infra.rabbit import Rabbit
from stbcore.schemas.rabbit import GenerateUserStatsInSchema


class RabbitRepositoryProtocol(Protocol):
  async def send_user_stats(self: Self, message: Message) -> None: ...


class RabbitRepositoryImpl:
  """
  """

  async def send_user_stats(self: Self, message: Message) -> None:
    """Publishes a message to send a user stats from the cache
    """
    await Rabbit.broker.publish(
      message=GenerateUserStatsInSchema(
        user_tg_id=message.from_user.id,
        message_tg_id=message.message_id,
      ),
      routing_key=RabbitRoutingKeysEnum.TG_MESSAGES__USER_STATS,
    )


RabbitRepository = RabbitRepositoryImpl()