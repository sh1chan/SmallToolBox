from typing import Self

import minio

from stbcore.core.config import settings
from stbcore.core.enums import MinioBucketsEmum


class Minio:
	client: minio.Minio | None = None

	@classmethod
	def initialize(cls: Self) -> None:
		cls.client = minio.Minio(
			endpoint=settings.minio.endpoint,
			access_key=settings.minio.access_key,
			secret_key=settings.minio.secret_key,
			secure=False,
			cert_check=False,
		)
		if not cls.client.bucket_exists(MinioBucketsEmum.userstats):
			cls.client.make_bucket(MinioBucketsEmum.userstats)

	@classmethod
	def terminate(cls: Self) -> None:	...