from pydantic import BaseModel


class UserStatsCacheSchema(BaseModel):
	minio_object_name: str