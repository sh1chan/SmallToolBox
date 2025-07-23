from typing import Protocol
from typing import Self

from stbcore.core.enums import MinioBucketsEmum
from stbcore.infra.minio import Minio


__all__ = (
	"MinioRepository",
	"MinioRepositoryProtocol",
)


class MinioRepositoryProtocol(Protocol):
	"""
	"""

	def read_user_stats_file(self: Self, filename: str) -> bytes:	...


class MinioRepositoryImpl:
	"""
	"""

	def read_user_stats_file(self: Self, filename: str) -> bytes:
		file_object = Minio.client.get_object(
			bucket_name=MinioBucketsEmum.userstats,
			object_name=filename,
		)
		return file_object.data


MinioRepository = MinioRepositoryImpl()