from typing import Protocol
from typing import Self


__all__ = (
	"RedisRepository",
	"RedisRepositoryProtocol",
)


class RedisRepositoryProtocol(Protocol):
	...


class RedisRepositoryImpl:
	...


RedisRepository = RedisRepositoryImpl()