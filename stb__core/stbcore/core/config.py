""" Core Config File
"""


__all__ = (
	"settings",
)


from pydantic import BaseModel
from pydantic import RedisDsn
from pydantic import AmqpDsn
from pydantic import PostgresDsn
from pydantic import computed_field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class TGBot(BaseModel):
	"""
	"""
	TOKEN: str

	@computed_field
	@property
	def token(self) -> str:
		"""
		"""
		return str(self.TOKEN)


class Redis(BaseModel):
	"""
	"""
	BROKER_URL: RedisDsn

	@computed_field
	@property
	def broker_url(self) -> str:
		"""
		"""
		return str(self.BROKER_URL)


class Rabbit(BaseModel):
	"""
	"""
	BROKER_URL: AmqpDsn

	@computed_field
	@property
	def broker_url(self) -> str:
		"""
		"""
		return str(self.BROKER_URL)


class Kafka(BaseModel):
	"""
	"""
	BOOTSTRAP_SERVERS: str

	@computed_field
	@property
	def bootstrap_servers(self) -> str:
		"""
		"""
		return str(self.BOOTSTRAP_SERVERS)


class Postgres(BaseModel):
	"""
	"""
	URL: PostgresDsn

	@computed_field
	@property
	def url(self) -> str:
		"""
		"""
		return str(self.URL)


class Minio(BaseModel):
	"""
	"""
	ENDPOINT: str
	ACCESS_KEY: str
	SECRET_KEY: str

	@computed_field
	@property
	def endpoint(self) -> str:
		"""
		"""
		return str(self.ENDPOINT)

	@computed_field
	@property
	def access_key(self) -> str:
		"""
		"""
		return str(self.ACCESS_KEY)

	@computed_field
	@property
	def secret_key(self) -> str:
		"""
		"""
		return str(self.SECRET_KEY)


class Settings(BaseSettings):
	"""
	"""
	tgbot: TGBot
	redis: Redis
	rabbit: Rabbit
	kafka: Kafka
	postgres: Postgres
	minio: Minio

	class Config(SettingsConfigDict):
		"""
		"""
		env_nested_delimiter = "__"


settings = Settings()