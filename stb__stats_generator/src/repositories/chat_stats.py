import io
from typing import Protocol
from typing import Self

import matplotlib.pyplot as plt

from stbcore.models.chat import ChatStats


__all__ = (
	"ChatStatsRepository",
	"ChatStatsRepositoryProtocol",
)


HOURS: tuple[int] = tuple(range(24))


class ChatStatsRepositoryProtocol(Protocol):
	"""
	"""

	def generate(
			self: Self,
			chat_stats: ChatStats | None,
	) -> io.BytesIO:	...


class ChatStatsRepositoryImpl:
	"""
	"""

	def generate(
			self: Self,
			chat_stats: ChatStats | None,
	) -> io.BytesIO:
		"""
		"""
		buf = io.BytesIO()
		users_count = []
		messages_count = []

		for hour in HOURS:
			uam = chat_stats.data["data"].get(hour, {})
			users_count.append(
				uam.get("users_count", 0)
			)
			messages_count.append(
				uam.get("messages_count", 0)
			)

		plt.plot(
			HOURS, users_count,
			color="C0", label="Users",
		)
		plt.plot(
			HOURS, messages_count,
			color="C1", label="Messages",
		)

		if chat_stats.data:
			plt.legend(title="")

		plt.grid(axis="y")
		plt.title(
			f"Users={chat_stats.users_count}, Messages={chat_stats.messages_count}",
		)
		plt.xlabel("24-hour clock")
		plt.ylabel("Sent Messages and Users count")
		plt.savefig(buf, format="png")
		plt.close()

		return buf


def get_chat_stats_repository() -> ChatStatsRepositoryProtocol:
	"""
	"""
	return ChatStatsRepositoryImpl()


ChatStatsRepository = get_chat_stats_repository()