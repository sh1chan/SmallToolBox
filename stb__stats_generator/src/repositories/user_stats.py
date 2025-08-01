import io
from typing import Protocol
from typing import Self

import matplotlib.pyplot as plt

from stbcore.models.user import UserStats


__all__ = (
	"UserStatsRepository",
	"UserStatsRepositoryProtocol",
)


HOURS: tuple[int] = tuple(range(24))


class UserStatsRepositoryProtocol(Protocol):
	"""
	"""

	def generate(
			self: Self,
			user_stats: UserStats | None,
	) -> io.BytesIO:	...


class UserStatsRepositoryImpl:
	"""
	"""

	def generate(
			self: Self,
			user_stats: UserStats,
	) -> io.BytesIO:
		"""
		"""
		buf = io.BytesIO()

		for cid, chat_data in enumerate(user_stats.data.values()):
			chat_name = chat_data["chat_name"]
			messages_count = []
			for hour in HOURS:
				mc = chat_data["data"].get(hour, 0)
				messages_count.append(mc)
			plt.plot(
				HOURS, messages_count,
				color=f"C{cid}", label=chat_name,
			)

		if user_stats.data:
			plt.legend(title="")

		plt.grid(axis="y")
		plt.title(
			f"Chats={user_stats.chats_count}, Messages={user_stats.messages_count}",
		)
		plt.xlabel("24-hour clock")
		plt.ylabel("Sent Messages count in Chats")
		plt.savefig(buf, format="webp")
		plt.close()

		return buf


def get_user_stats_repository() -> UserStatsRepositoryProtocol:
	"""
	"""
	return UserStatsRepositoryImpl()


UserStatsRepository = get_user_stats_repository()