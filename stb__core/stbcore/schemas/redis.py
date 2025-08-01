""" Redis Schemas
"""


__all__ = (
	"UserStatsCacheSchema",
	"ChatStatsCacheSchema",
)


from pydantic import BaseModel
from pydantic import PositiveInt
from pydantic import NegativeInt


class UserStatsCacheSchema(BaseModel):
	"""
	"""
	user_tg_id: PositiveInt
	minio_object_name: str


class ChatStatsCacheSchema(BaseModel):
	"""
	"""
	chat_tg_id: NegativeInt
	minio_object_name: str