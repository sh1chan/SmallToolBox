""" Chat Related Models
"""


__all__ = (
	"Chat",
	"ChatSettings",
	"ChatStats",
)


from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy import BigInteger
from sqlalchemy import Boolean
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from stbcore.models.base import Base

# TODO (ames0k0)
#	- Add `Model` suffix, e.g. `ChatModel`
# - Use `Date` Type


class Chat(Base):
	""" Telegram Chat Object
	"""
	__tablename__ = "tgbot_chat"

	id: Mapped[int] = mapped_column(
		BigInteger, nullable=False, primary_key=True
	)
	username: Mapped[Optional[str]]
	full_name: Mapped[str]

	# Relations
	message_settings: Mapped["ChatSettings"] = relationship(
		back_populates="chat",
		lazy="selectin",
	)


class ChatSettings(Base):
	__tablename__ = "tgbot_chat_settings"

	id: Mapped[int] = mapped_column(primary_key=True)

	# Settings
	save_stats: Mapped[bool] = mapped_column(
		Boolean, nullable=False, server_default='t'
	)

	# Relations
	chat_id: Mapped[int] = mapped_column(ForeignKey("tgbot_chat.id"))
	chat: Mapped["Chat"] = relationship(back_populates="message_settings")


class ChatStats(Base):
	""" Daily Cache
	"""
	__tablename__ = "tgbot_chat_stats"

	id: Mapped[int] = mapped_column(primary_key=True)
	date: Mapped[str]

	users_count: Mapped[int] = mapped_column(
		BigInteger, nullable=False, server_default="0"
	)
	messages_count: Mapped[int] = mapped_column(
		BigInteger, nullable=False, server_default="0"
	)
	data: Mapped[dict] = mapped_column(
		JSON, nullable=False, server_default="{}"
	)
	report_filepath: Mapped[str]

	# Relations
	chat_id: Mapped[int] = mapped_column(ForeignKey("tgbot_chat.id"))