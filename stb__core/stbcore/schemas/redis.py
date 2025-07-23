from pydantic import BaseModel
from pydantic import PositiveInt


class UserStatsCacheSchema(BaseModel):
	user_tg_id: PositiveInt
	minio_object_name: str