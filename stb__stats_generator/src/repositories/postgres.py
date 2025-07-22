from typing import Protocol
from typing import Self
from typing import Sequence


__all__ = (
	"PostgresRepository",
	"PostgresRepositoryProtocol",
)


class PostgresRepositoryProtocol(Protocol):
	...


class PostgresRepositoryImpl:
	...


PostgresRepository = PostgresRepositoryImpl()