import io
import tempfile

import matplotlib.pyplot as plt


HOURS = (
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    21,
    22,
    23,
)


def default(user_stats):
    title_tmp = "Chats={CHAT_COUNT}, Messages={MESSAGE_COUNT}"
    buf = io.BytesIO()
    for cid, chat_data in enumerate(user_stats.data.values()):
        chat_name = chat_data["chat_name"]
        messages_count = []
        for hour in HOURS:
            mc = chat_data["data"].get(hour, 0)
            messages_count.append(mc)
        plt.plot(
            HOURS,
            messages_count,
            color=f"C{cid}",
            label=chat_name,
        )
    plt.grid(axis="y")
    plt.legend(title="")
    plt.title(
        title_tmp.format(
            CHAT_COUNT=user_stats.chats_count,
            MESSAGE_COUNT=user_stats.messages_count,
        )
    )
    plt.xlabel("24-hour clock")
    plt.ylabel("Sent Messages count in Chats")
    plt.savefig(buf, format="webp")
    with tempfile.NamedTemporaryFile(
        suffix=".webp",
        delete=False,
    ) as ftw:
        ftw.write(buf.getvalue())
        plt.close()
        buf.close()
        ftw.close()
        return ftw.name
