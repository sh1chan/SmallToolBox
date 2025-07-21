from sqlalchemy import ForeignKey
from sqlalchemy import BigInteger
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from stbcore.models.base import Base


class Message(Base):
	""" Telegram Message Object
	"""
	__tablename__ = "tgbot_message"

	id: Mapped[int] = mapped_column(primary_key=True)

	message_id: Mapped[int]
	date: Mapped[str]

	# Relations
	user_id: Mapped[int] = mapped_column(ForeignKey("tgbot_user.id"))
	chat_id: Mapped[int] = mapped_column(ForeignKey("tgbot_chat.id"))


class MessageStats(Base):
	__tablename__ = "tgbot_message_stats"

	id: Mapped[int] = mapped_column(primary_key=True)

	message_count: Mapped[int] = mapped_column(
		BigInteger, nullable=False, server_default="0"
	)
	date: Mapped[str] = mapped_column(
		String, nullable=False
	)

	# Relations
	user_id: Mapped[int] = mapped_column(ForeignKey("tgbot_user.id"))
	chat_id: Mapped[int] = mapped_column(ForeignKey("tgbot_chat.id"))
