import io
import tempfile

import matplotlib.pyplot as plt


HOURS = (
  0,
  1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
  11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
  21, 22, 23
)


def default(cs):
  users_count = []
  messages_count = []
  for hour in HOURS:
    uam = cs.data["data"].get(hour)
    if not uam:
      users_count.append(0)
      messages_count.append(0)
      continue
    users_count.append(
      uam.get("users_count", 0)
    )
    messages_count.append(
      uam.get("messages_count", 0)
    )

  plt.plot(
    HOURS, users_count,
    color="C0", label="Users",
  )
  plt.plot(
    HOURS, messages_count,
    color="C1", label="Messages",
  )
  plt.legend(title="")
  plt.grid(axis="y")
  plt.title(
    f"Users={cs.users_count}, Messages={cs.messages_count}"
  )
  plt.xlabel("24-hour clock")
  plt.ylabel("Sent Messages and Users count")
  buf = io.BytesIO()
  plt.savefig(buf, format="png")
  with tempfile.NamedTemporaryFile(
      suffix=".png",
      delete=False,
  ) as ftw:
    ftw.write(buf.getvalue())
    plt.close()
    buf.close()
    ftw.close()
    return ftw.name