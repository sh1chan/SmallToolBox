from routes.root.router import root_router
from routes.user.router import user_router
from routes.chat.router import chat_router


routers = [
	root_router,
	user_router,
	chat_router,
]