""" User Related Models
"""


__all__ = (
	"User",
	"UserSettings",
	"UserStats",
)


from typing import List
from typing import TYPE_CHECKING
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy import BigInteger
from sqlalchemy import Boolean
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from stbcore.models.base import Base


if TYPE_CHECKING:
	from stbcore.models.message import Message


class User(Base):
	""" Telegram User Object
	"""
	__tablename__ = "tgbot_user"

	id: Mapped[int] = mapped_column(
		BigInteger, nullable=False, primary_key=True
	)
	username: Mapped[Optional[str]]
	full_name: Mapped[str]

	# Relations
	message_settings: Mapped["UserSettings"] = relationship(
		back_populates="user",
		lazy="selectin",
	)
	messages: Mapped[List["Message"]] = relationship()


class UserSettings(Base):
	"""
	"""
	__tablename__ = "tgbot_user_settings"

	id: Mapped[int] = mapped_column(primary_key=True)

	# Settings
	save_messages: Mapped[bool] = mapped_column(
		Boolean, nullable=False, server_default='f'
	)
	save_stats: Mapped[bool] = mapped_column(
		Boolean, nullable=False, server_default='t'
	)

	# Relations
	user_id: Mapped[int] = mapped_column(ForeignKey("tgbot_user.id"))
	user: Mapped["User"] = relationship(back_populates="message_settings")


class UserChat(Base):
	"""
	"""
	__tablename__ = "tgbot_user_chat"

	id: Mapped[int] = mapped_column(
		BigInteger, nullable=False, primary_key=True
	)

	is_user_admin: Mapped[bool] = mapped_column(
		Boolean, nullable=False, server_default="t"
	)

	# Relations
	user_id: Mapped[int] = mapped_column(ForeignKey("tgbot_user.id"))
	chat_id: Mapped[int] = mapped_column(ForeignKey("tgbot_chat.id"))


class UserStats(Base):
	""" Cache
	"""
	__tablename__ = "tgbot_user_stats"

	id: Mapped[int] = mapped_column(primary_key=True)
	date: Mapped[str]

	chats_count: Mapped[int] = mapped_column(
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
	user_id: Mapped[int] = mapped_column(ForeignKey("tgbot_user.id"))