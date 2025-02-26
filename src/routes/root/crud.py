from sqlalchemy import select

from . import models, utils


class User:
    @staticmethod
    async def get(session, user_id):
        return (
            await session.execute(
                select(models.User).where(
                    models.User.id == user_id,
                )
            )
        ).scalar()

    async def insert(self, session, tg_user):
        db_user = await self.get(session, tg_user.id)
        if db_user:
            return db_user
        db_user = models.User(
            id=tg_user.id,
            username=tg_user.username,
            full_name=tg_user.full_name,
        )
        session.add(db_user)
        await session.commit()
        return db_user


class UserSettings:
    @staticmethod
    async def get(session, user_id):
        return (
            await session.execute(
                select(models.UserSettings).where(
                    models.UserSettings.user_id == user_id
                )
            )
        ).scalar()

    async def insert(self, session, user_id):
        user_message_settings = await self.get(session, user_id)
        if user_message_settings:
            return user_message_settings
        user_message_settings = models.UserSettings(user_id=user_id)
        session.add(user_message_settings)
        await session.commit()
        return user_message_settings

    async def apply(
        self,
        session,
        tg_message,
        db_user,
        db_chat,
    ):
        user_message_settings = await self.insert(
            session=session,
            user_id=db_user.id,
        )
        if user_message_settings.save_messages:
            await Message().insert(
                session=session,
                tg_message=tg_message,
                db_user_id=db_user.id,
                db_chat_id=db_chat.id,
            )

        return user_message_settings


class Chat:
    @staticmethod
    async def get(session, chat_id):
        return (
            await session.execute(
                select(models.Chat).where(
                    models.Chat.id == chat_id,
                )
            )
        ).scalar()

    async def insert(self, session, tg_chat):
        db_chat = await self.get(session, tg_chat.id)
        if db_chat:
            return db_chat
        chat = models.Chat(
            id=tg_chat.id,
            username=tg_chat.username,
            full_name=tg_chat.full_name,
        )
        session.add(chat)
        await session.commit()
        return chat


class ChatSettings:
    @staticmethod
    async def get(session, chat_id):
        return (
            await session.execute(
                select(models.ChatSettings).where(
                    models.ChatSettings.chat_id == chat_id
                )
            )
        ).scalar()

    async def insert(self, session, chat_id):
        chat_message_settings = await self.get(session, chat_id)
        if chat_message_settings:
            return chat_message_settings
        chat_message_settings = models.ChatSettings(chat_id=chat_id)
        session.add(chat_message_settings)
        await session.commit()
        return chat_message_settings

    async def apply(
        self,
        session,
        db_chat,
    ):
        return await self.insert(
            session=session,
            chat_id=db_chat.id,
        )


class Message:
    @staticmethod
    async def insert(session, tg_message, db_user_id, db_chat_id):
        db_message = models.Message(
            message_id=tg_message.message_id,
            date=utils.utc2date(tg_message.date),
            user_id=db_user_id,
            chat_id=db_chat_id,
        )
        session.add(db_message)
        await session.commit()


class MessageStats:
    @staticmethod
    async def get(session, user_id, chat_id, date):
        return (
            await session.execute(
                select(models.MessageStats).where(
                    models.MessageStats.user_id == user_id,
                    models.MessageStats.chat_id == chat_id,
                    models.MessageStats.date == date,
                )
            )
        ).scalar()

    @staticmethod
    async def get_by_date(session, user_id=None, chat_id=None, date=None):
        if not any((user_id, chat_id)):
            raise ValueError("User or Chat id is required!")
        # without hour
        date = date.split()[0]
        filters = [models.MessageStats.date.startswith(date)]
        if user_id:
            filters.append(models.MessageStats.user_id == user_id)
        if chat_id:
            filters.append(models.MessageStats.chat_id == chat_id)
        return (
            await session.execute(
                select(models.MessageStats)
                .where(*filters)
                .order_by(models.MessageStats.id)
            )
        ).scalars()

    async def update(
        self,
        session,
        tg_message,
        db_user,
        db_chat,
    ):
        date = tg_message.date.strftime("%Y-%m-%d %H")
        db_message_stats = await self.get(
            session=session,
            user_id=db_user.id,
            chat_id=db_chat.id,
            date=date,
        )
        if db_message_stats:
            db_message_stats.message_count += 1
        else:
            db_message_stats = models.MessageStats(
                date=date,
                message_count=1,
                user_id=db_user.id,
                chat_id=db_chat.id,
            )
            session.add(db_message_stats)

        await session.commit()


class MessageSettings:
    """User and Chat Message Settings

    - Check if User not equal to Chat

    User
      - check user_message_settings
        - save_messages
        - save_stats
    Chat
      - check chat_message_settings
        - save_stats
    """

    @staticmethod
    async def apply(session, tg_user, tg_chat, tg_message):
        if tg_user.id == tg_chat.id:
            return
        db_user = await User().insert(session=session, tg_user=tg_user)
        db_chat = await Chat().insert(session=session, tg_chat=tg_chat)

        user_manage_settings = await UserSettings().apply(
            session=session,
            tg_message=tg_message,
            db_user=db_user,
            db_chat=db_chat,
        )
        chat_message_settings = await ChatSettings().apply(
            session=session,
            db_chat=db_chat,
        )
        if any(
            (
                user_manage_settings.save_stats,
                chat_message_settings.save_stats,
            )
        ):
            await MessageStats().update(
                session=session,
                tg_message=tg_message,
                db_user=db_user,
                db_chat=db_chat,
            )
