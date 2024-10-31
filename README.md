# Issue Tracker: Project Sage0x0

Interface:
  - TelegramBot: https://t.me/smalltoolboxbot
    - Main Channel: https://t.me/smalltoolbox

<div align="center">
  <img src="./static/readme/TgBot.png" />
</div>


#### TODO
- Merge `UserStats` and `ChatStats` as `MessageStats` ??
```
stb=# select  *from tgbot_chat_stats;
 id | message_count |     date      |  user_id  |    chat_id
----+---------------+---------------+-----------+----------------
  1 |             7 | 2024-10-31 04 | 407886247 | -1002315205609
(1 row)

stb=# select * from tgbot_user_stats;
 id | message_count |     date      |  user_id  |    chat_id
----+---------------+---------------+-----------+----------------
  1 |             7 | 2024-10-31 04 | 407886247 | -1002315205609
(1 row)
```
