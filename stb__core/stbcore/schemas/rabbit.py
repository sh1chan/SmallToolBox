""" RabbitMQ Schemas
"""


__all__ = (
	"GenerateStatsSchema",
)


from datetime import datetime

from pydantic import BaseModel
from pydantic import PositiveInt
from pydantic import NegativeInt


class GenerateStatsSchema(BaseModel):
	"""
	"""
	chat_tg_id: NegativeInt
	user_tg_id: PositiveInt
	message_tg_id: PositiveInt
	message_date: datetime