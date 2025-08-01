""" MinIO Infra
"""


__all__ = (
	"Minio",
)


from typing import Self

import minio

from stbcore.core.config import settings
from stbcore.core.enums import MinioBucketsEmum


class Minio:
	"""
	"""
	client: minio.Minio | None = None

	@classmethod
	def initialize(cls: Self) -> None:
		"""
		"""
		cls.client = minio.Minio(
			endpoint=settings.minio.endpoint,
			access_key=settings.minio.access_key,
			secret_key=settings.minio.secret_key,
			secure=False,
			cert_check=False,
		)

		for bucket_name in (
				MinioBucketsEmum.userstats,
				MinioBucketsEmum.chatstats,
		):
			if cls.client.bucket_exists(bucket_name=bucket_name):
				continue
			cls.client.make_bucket(bucket_name=bucket_name)

	@classmethod
	def terminate(cls: Self) -> None:
		"""
		"""