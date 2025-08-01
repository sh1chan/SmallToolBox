""" Routes Package
"""


__all__ = (
	"routers",
)


from .root.router import root_router
from .user.router import user_router
from .chat.router import chat_router


routers = [
	user_router,
	chat_router,
	root_router,
]