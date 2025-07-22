from pydantic import BaseModel
from pydantic import PositiveInt


class UserStatsIn(BaseModel):
	user_tg_id: PositiveInt