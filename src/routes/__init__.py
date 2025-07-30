from .root.router import root_router
from .user.router import user_router
from .chat.router import chat_router


routers = [
	root_router,
	user_router,
	chat_router,
]