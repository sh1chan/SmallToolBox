""" Base Models
"""


__all__ = (
	"Base",
)


from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
	"""
	"""