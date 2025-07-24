from pydantic import BaseModel
from pydantic import PositiveInt
from pydantic import NegativeInt


class MessageEventSchema(BaseModel):
	user_tg_id: PositiveInt
	chat_tg_id: NegativeInt
	message_tg_id: PositiveInt
	date: str