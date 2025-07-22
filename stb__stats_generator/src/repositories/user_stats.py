from typing import Protocol
from typing import Self


__all__ = (
	"UserStatsRepository",
	"UserStatsRepositoryProtocol",
)


class UserStatsRepositoryProtocol(Protocol):
	...


class UserStatsRepositoryImpl:
	...


UserStatsRepository = UserStatsRepositoryImpl()