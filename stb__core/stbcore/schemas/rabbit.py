from pydantic import BaseModel
from pydantic import PositiveInt


class GenerateUserStatsInSchema(BaseModel):
	user_tg_id: PositiveInt
	message_tg_id: PositiveInt