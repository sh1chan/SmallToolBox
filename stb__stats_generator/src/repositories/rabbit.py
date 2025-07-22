from typing import Protocol
from typing import Self


__all__ = (
	"RabbitRepository",
	"RabbitRepositoryProtocol",
)


class RabbitRepositoryProtocol(Protocol):
	...


class RabbitRepositoryImpl:
	...


RabbitRepository = RabbitRepositoryImpl()