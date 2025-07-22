from enum import StrEnum
from enum import auto


class RabbitRoutingKeysEnum(StrEnum):
	STATS_GENERATOR__USER_STATS = auto()
	TG_MESSAGES__USER_STATS = auto()