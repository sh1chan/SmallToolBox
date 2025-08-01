""" Root Router Repository
"""


__all__ = (
	"RootRepository",
	"RootRepositoryProtocol",
)


from typing import Protocol
from typing import Self

from aiogram.types import Message

from stbcore.schemas.kafka import TelegramUserObjectSchema
from stbcore.schemas.kafka import TelegramChatObjectSchema
from stbcore.schemas.kafka import TelegramMessageObjectSchema
from stbcore.schemas.kafka import TelegramMessageEventSchema

from .kafka import KafkaRepository
from .kafka import KafkaRepositoryProtocol


class RootRepositoryProtocol(Protocol):
	"""
	"""

	def __init__(
			self: Self,
			kafka_repository: KafkaRepositoryProtocol,
	) -> None:	...

	async def register_message(self: Self, message: Message) -> None:	...


class RootRepositoryImpl:
	"""
	"""

	def __init__(
			self: Self,
			kafka_repository: KafkaRepositoryProtocol
	) -> None:
		self.kafka_repository = kafka_repository

	async def register_message(self: Self, message: Message) -> None:
		"""
		"""
		await self.kafka_repository.publish_event(
			payload=TelegramMessageEventSchema(
				user=TelegramUserObjectSchema(
					tg_id=message.from_user.id,
					username=message.from_user.username,
					full_name=message.from_user.full_name,
				),
				chat=TelegramChatObjectSchema(
					tg_id=message.chat.id,
					username=message.chat.username,
					full_name=message.chat.full_name,
				),
				message=TelegramMessageObjectSchema(
					tg_id=message.message_id,
					date=message.date.strftime("%Y-%m-%d %H:%M:%S"),
				),
			)
		)


def get_root_repository() -> RootRepositoryProtocol:
	"""
	"""
	return RootRepositoryImpl(
		kafka_repository=KafkaRepository,
	)


RootRepository = get_root_repository()