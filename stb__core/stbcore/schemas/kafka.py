""" Apache Kafka Schemas
"""


__all__ = (
	"TelegramUserObjectSchema",
	"TelegramChatObjectSchema",
	"TelegramMessageObjectSchema",
	"TelegramMessageEventSchema",
)


from pydantic import BaseModel
from pydantic import PositiveInt
from pydantic import NegativeInt


class TelegramUserObjectSchema(BaseModel):
	"""
	"""
	tg_id: PositiveInt
	username: str | None
	full_name: str


class TelegramChatObjectSchema(BaseModel):
	"""
	"""
	tg_id: NegativeInt
	username: str | None
	full_name: str


class TelegramMessageObjectSchema(BaseModel):
	"""
	"""
	tg_id: PositiveInt
	date: str


class TelegramMessageEventSchema(BaseModel):
	"""
	"""
	user: TelegramUserObjectSchema
	chat: TelegramChatObjectSchema
	message: TelegramMessageObjectSchema