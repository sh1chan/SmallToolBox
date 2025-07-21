from pydantic import BaseModel
from pydantic import RedisDsn
from pydantic import AmqpDsn
from pydantic import PostgresDsn
from pydantic import AnyUrl


class settings(BaseModel):
	REDIS__BROKER_URL: RedisDsn = "redis://localhost:6379/"
	RABBIT__BROKER_URL: AmqpDsn = "amqp://guest:guest@localhost:5672/"
	KAFKA__BOOTSTRAP_SERVERS: AnyUrl = ""
	POSTGRES__URL: PostgresDsn

	@property
	def redis_broker_url(self):
		return str(self.REDIS__BROKER_URL)

	@property
	def rabbit_broker_url(self):
		return str(self.RABBIT__BROKER_URL)

	@property
	def kafka_bootstrap_servers(self):
		return str(self.KAFKA__BOOTSTRAP_SERVERS)

	@property
	def postgres_url(self):
		return str(self.POSTGRES__URL)