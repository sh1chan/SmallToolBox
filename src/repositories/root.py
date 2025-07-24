from typing import Protocol
from typing import Self

from aiogram.types import Message

from stbcore.schemas.kafka import MessageEventSchema

from .kafka import KafkaRepository
from .kafka import KafkaRepositoryProtocol


class RootRepositoryProtocol(Protocol):
	"""
	"""

	def __init__(
			self: Self,
			kafka_repository: KafkaRepositoryProtocol,
	):	...

	async def register_message(self: Self, message: Message) -> None:	...


class RootRepositoryImpl:
	"""
	"""

	def __init__(
			self: Self,
			kafka_repository: KafkaRepositoryProtocol
	):
		self.kafka_repository = kafka_repository

	async def register_message(self: Self, message: Message) -> None:
		await self.kafka_repository.publish_event(
			payload=MessageEventSchema(
				user_tg_id=message.from_user.id,
				chat_tg_id=message.chat.id,
				message_tg_id=message.message_id,
				date=message.date.strftime("%Y-%m-%d %H:%M:%S"),
			)
		)


def get_root_repository() -> RootRepositoryProtocol:
	return RootRepositoryImpl(
		kafka_repository=KafkaRepository,
	)


RootRepository = get_root_repository()