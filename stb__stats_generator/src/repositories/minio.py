from typing import Protocol
from typing import Self

from stbcore.infra.minio import Minio
from stbcore.core.enums import MinioBucketsEmum


__all__ = (
	"MinioRepository",
	"MinioRepositoryProtocol",
)


class MinioRepositoryProtocol(Protocol):
	"""
	"""

	def create_user_stats_file(self: Self, filename: str, file_in_bytes: bytes) -> None:	...

	def delete_user_stats_file(self: Self, filename: str) -> None:	...


class MinioRepositoryImpl:
	"""
	"""

	def create_user_stats_file(self: Self, filename: str, file_as_bytes: bytes) -> None:
		Minio.client.put_object(
			bucket_name=MinioBucketsEmum.user_stats,
			object_name=filename,
			data=file_as_bytes,
		)

	def delete_user_stats_file(self: Self, filename: str) -> None:
		Minio.client.remove_object(
			bucket_name=MinioBucketsEmum.user_stats,
			object_name=filename
		)


MinioRepository = MinioRepositoryImpl()