from typing import List, Optional

from sqlalchemy import (
  ForeignKey, Column,
  BigInteger, Boolean, String,
)
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.sql.db import Base


class User(Base):
  """ Telegram User Object
  """
  __tablename__ = "tgbot_user"

  id: Mapped[int] = Column(
    BigInteger, nullable=False, primary_key=True
  )
  username: Mapped[Optional[str]]
  full_name: Mapped[str]

  # Relations
  message_settings: Mapped["UserSettings"] = relationship(back_populates="user")
  messages: Mapped[List["Message"]] = relationship()


class UserChat(Base):
  __tablename__ = "tgbot_user_chat"

  id: Mapped[int] = Column(
    BigInteger, nullable=False, primary_key=True
  )

  is_user_admin: Mapped[bool] = Column(
    Boolean, nullable=False, server_default="t"
  )

  # Relations
  user_id: Mapped[int] = mapped_column(ForeignKey("tgbot_user.id"))
  chat_id: Mapped[int] = mapped_column(ForeignKey("tgbot_chat.id"))


class UserSettings(Base):
  __tablename__ = "tgbot_user_settings"

  id: Mapped[int] = mapped_column(primary_key=True)

  # Settings
  save_messages: Mapped[bool] = Column(
    Boolean, nullable=False, server_default='f'
  )
  save_stats: Mapped[bool] = Column(
    Boolean, nullable=False, server_default='t'
  )

  # Relations
  user_id: Mapped[int] = mapped_column(ForeignKey("tgbot_user.id"))
  user: Mapped["User"] = relationship(back_populates="message_settings")


class Chat(Base):
  """ Telegram Chat Object
  """
  __tablename__ = "tgbot_chat"

  id: Mapped[int] = Column(
    BigInteger, nullable=False, primary_key=True
  )
  username: Mapped[Optional[str]]
  full_name: Mapped[str]

  # Relations
  message_settings: Mapped["ChatSettings"] = relationship(back_populates="chat")


class ChatSettings(Base):
  __tablename__ = "tgbot_chat_settings"

  id: Mapped[int] = mapped_column(primary_key=True)

  # Settings
  save_stats: Mapped[bool] = Column(
    Boolean, nullable=False, server_default='t'
  )

  # Relations
  chat_id: Mapped[int] = mapped_column(ForeignKey("tgbot_chat.id"))
  chat: Mapped["Chat"] = relationship(back_populates="message_settings")


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

  message_count: Mapped[int] = Column(
    BigInteger, nullable=False, server_default="0"
  )
  date: Mapped[str] = Column(
    String, nullable=False
  )

  # Relations
  user_id: Mapped[int] = mapped_column(ForeignKey("tgbot_user.id"))
  chat_id: Mapped[int] = mapped_column(ForeignKey("tgbot_chat.id"))
