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

	def generate(self: Self, hourly_user_stats: UserStats | None) -> io.BytesIO:	...


class UserStatsRepositoryImpl:
	"""
	"""

	def generate(self: Self, hourly_user_stats: UserStats | None) -> io.BytesIO:
		buf = io.BytesIO()

		if not hourly_user_stats:
			plt.title(f"Chats=0, Messages=0")
			plt.plot(
				HOURS,
				[0] * len(HOURS),
				color=f"C0",
			)
		else:
			plt.legend(title="")
			plt.title(
				f"Chats={hourly_user_stats.chats_count}, Messages={hourly_user_stats.messages_count}"
			)
			for cid, chat_data in enumerate(hourly_user_stats.data.values()):
				chat_name = chat_data["chat_name"]
				messages_count = []
				for hour in HOURS:
					mc = chat_data["data"].get(hour, 0)
					messages_count.append(mc)
				plt.plot(
					HOURS, messages_count,
					color=f"C{cid}", label=chat_name,
				)

		plt.grid(axis="y")
		plt.xlabel("24-hour clock")
		plt.ylabel("Sent Messages count in Chats")
		plt.savefig(buf, format="webp")

		return buf


UserStatsRepository = UserStatsRepositoryImpl()