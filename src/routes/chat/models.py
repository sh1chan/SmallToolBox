from sqlalchemy import (
	ForeignKey, Column,
	BigInteger, JSON,
)
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from stbcore.models.base import Base


class ChatStats(Base):
	"""Cache
	"""
	__tablename__ = "tgbot_chat_stats"

	id: Mapped[int] = mapped_column(primary_key=True)
	date: Mapped[str]

	users_count: Mapped[int] = Column(
		BigInteger, nullable=False, server_default="0"
	)
	messages_count: Mapped[int] = Column(
		BigInteger, nullable=False, server_default="0"
	)
	data: Mapped[dict] = Column(
		JSON, nullable=False, server_default="{}"
	)
	report_filepath: Mapped[str]

	# Relations
	chat_id: Mapped[int] = mapped_column(ForeignKey("tgbot_chat.id"))
