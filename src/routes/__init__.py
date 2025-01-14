from . import root, user, chat


routers = [
  user.router,
  chat.router,
  root.router,
]
