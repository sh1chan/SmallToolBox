from pydantic import BaseModel


class UserStatsCacheSchema(BaseModel):
	MINIO_OBJECT_DST = str