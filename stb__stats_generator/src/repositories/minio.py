import io
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

	def create_user_stats_file(
			self: Self,
			filename: str,
			file_as_bytes: io.BytesIO,
	) -> None:	...

	def create_chat_stats_file(
			self: Self,
			filename: str,
			file_as_bytes: io.BytesIO,
	) -> None:	...

	def delete_user_stats_file(
			self: Self,
			filename: str,
	) -> None:	...

	def delete_chat_stats_file(
			self: Self,
			filename: str,
	) -> None:	...


class MinioRepositoryImpl:
	"""
	"""

	def create_user_stats_file(
			self: Self,
			filename: str,
			file_as_bytes: io.BytesIO,
	) -> None:
		"""
		"""
		file_length = file_as_bytes.getbuffer().nbytes
		file_as_bytes.seek(0)

		Minio.client.put_object(
			bucket_name=MinioBucketsEmum.userstats,
			object_name=filename,
			data=file_as_bytes,
			length=file_length,
		)

	def create_chat_stats_file(
			self: Self,
			filename: str,
			file_as_bytes: io.BytesIO,
	) -> None:
		"""
		"""
		file_length = file_as_bytes.getbuffer().nbytes
		file_as_bytes.seek(0)

		Minio.client.put_object(
			bucket_name=MinioBucketsEmum.chatstats,
			object_name=filename,
			data=file_as_bytes,
			length=file_length,
		)

	def delete_user_stats_file(
			self: Self,
			filename: str,
	) -> None:
		"""
		"""
		Minio.client.remove_object(
			bucket_name=MinioBucketsEmum.userstats,
			object_name=filename
		)

	def delete_chat_stats_file(
			self: Self,
			filename: str,
	) -> None:
		"""
		"""
		Minio.client.remove_object(
			bucket_name=MinioBucketsEmum.chatstats,
			object_name=filename,
		)


def get_minio_repository() -> MinioRepositoryProtocol:
	"""
	"""
	return MinioRepositoryImpl()


MinioRepository = get_minio_repository()