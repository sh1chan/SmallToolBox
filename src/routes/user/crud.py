from collections import defaultdict
from itertools import groupby

from sqlalchemy import select

from . import models
from src.routes.root import models as root_models
from src.routes.root.crud import Chat, MessageStats


class UserStats:
    @staticmethod
    async def get(session, user_id, date):
        return (
            await session.execute(
                select(models.UserStats).where(
                    models.UserStats.user_id == user_id,
                    models.UserStats.date == date,
                )
            )
        ).scalar()

    @staticmethod
    async def insert(
        session,
        user_id,
        date,
        data,
        all_chats_count,
        all_messages_count,
    ):
        us = models.UserStats(
            user_id=user_id,
            date=date,
            chats_count=all_chats_count,
            messages_count=all_messages_count,
            data=data,
            report_filepath="fake",
        )
        session.add(us)
        await session.commit()
        return us

    async def generate(self, session, user_id, date):
        data = await MessageStats.get_by_date(session, user_id=user_id, date=date)
        gen_data = defaultdict(dict)

        def grouper(message_stats):
            return message_stats.chat_id

        all_chats_count = 0
        all_messages_count = 0
        for chat_id, chat_ms in groupby(data, key=grouper):
            all_chats_count += 1
            chat = await Chat.get(session, chat_id)
            messages_count = {}
            for ms in chat_ms:
                all_messages_count += ms.message_count
                messages_count[int(ms.date.split()[1])] = ms.message_count
            gen_data[chat_id]["chat_name"] = chat.full_name
            gen_data[chat_id]["data"] = messages_count

        if not gen_data:
            return None

        return await self.insert(
            session=session,
            user_id=user_id,
            date=date,
            data=gen_data,
            all_chats_count=all_chats_count,
            all_messages_count=all_messages_count,
        )


class ProgressBar:
    @staticmethod
    async def get(session, user_id):
        # FIXME: LIMIT `5`
        return (
            await session.scalars(
                select(root_models.ProgressBar)
                .where(
                    root_models.ProgressBar.user_id == user_id,
                )
                .order_by(root_models.ProgressBar.id)
                .limit(5)
            )
        ).all()

    # @staticmethod
    # async def insert(
    #   session, user_id, date, data,
    #   all_chats_count, all_messages_count,
    # ):
