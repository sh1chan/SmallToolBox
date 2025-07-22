from typing import Protocol
from typing import Self


__all__ = (
	"MinioRepository",
	"MinioRepositoryProtocol",
)


class MinioRepositoryProtocol(Protocol):
	...


class MinioRepositoryImpl:
	...


MinioRepository = MinioRepositoryImpl()