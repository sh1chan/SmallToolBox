from typing import Self

import minio

from stbcore.core.config import settings


class Minio:
	client: minio.Minio | None = None

	@classmethod
	def initialize(cls: Self) -> None:
		cls.client = minio.Minio(
			endpoint=settings.minio.endpoint,
			access_key=settings.minio.access_key,
			secret_key=settings.minio.secret_key,
		)

	@classmethod
	def terminate(cls: Self) -> None:	...