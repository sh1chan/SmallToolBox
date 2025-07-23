from enum import Enum
from enum import StrEnum
from enum import auto


class RabbitRoutingKeysEnum(StrEnum):
	STATS_GENERATOR__USER_STATS = auto()
	TG_MESSAGES__USER_STATS = auto()


class MinioBucketsEmum(StrEnum):
	userstats = auto()


class RedisCacheNamesEnum(str, Enum):
	USER_STATS = "user_stats:{user_tg_id}:{datetime}"