from itertools import groupby

from sqlalchemy import select

from . import models
from src.routes.root.crud import Chat, MessageStats


class UserStats:
    @staticmethod
    async def get(session, chat_id, date):
        return (
            await session.execute(
                select(models.ChatStats).where(
                    models.ChatStats.chat_id == chat_id,
                    models.ChatStats.date == date,
                )
            )
        ).scalar()

    @staticmethod
    async def insert(
        session,
        chat_id,
        date,
        data,
        all_users_count,
        all_messages_count,
    ):
        us = models.ChatStats(
            chat_id=chat_id,
            date=date,
            users_count=all_users_count,
            messages_count=all_messages_count,
            data=data,
            report_filepath="fake",
        )
        session.add(us)
        await session.commit()
        return us

    async def generate(self, session, chat_id, date):
        data = await MessageStats.get_by_date(session, chat_id=chat_id, date=date)
        chat = await Chat.get(session, chat_id)
        gen_data = {
            "chat_name": chat.full_name,
            "users_count": 0,
            "messages_count": 0,
            "data": {},
        }

        def grouper(message_stats):
            return message_stats.date

        all_users_count = set()
        all_messages_count = 0
        for date_value, date_ms in groupby(data, key=grouper):
            users_count = set()
            messages_count = 0
            for ms in date_ms:
                users_count.add(ms.user_id)
                messages_count += ms.message_count
            all_messages_count += messages_count
            gen_data["data"][int(date_value.split()[1])] = {
                "users_count": len(users_count),
                "messages_count": messages_count,
            }
            all_users_count.update(users_count)
            users_count.clear()
        gen_data["users_count"] = len(all_users_count)
        gen_data["messages_count"] = all_messages_count

        if not all_messages_count:
            return None

        return await self.insert(
            session=session,
            chat_id=chat_id,
            date=date,
            data=gen_data,
            all_users_count=len(all_users_count),
            all_messages_count=all_messages_count,
        )
