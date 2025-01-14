from sqlalchemy import (
  ForeignKey, Column,
  BigInteger, JSON,
)
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.sql.db import Base


class UserStats(Base):
  """Cache
  """
  __tablename__ = "tgbot_user_stats"

  id: Mapped[int] = mapped_column(primary_key=True)
  date: Mapped[str]

  chats_count: Mapped[int] = Column(
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
  user_id: Mapped[int] = mapped_column(ForeignKey("tgbot_user.id"))
