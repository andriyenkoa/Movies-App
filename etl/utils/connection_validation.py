from pydantic_settings import BaseSettings
from pydantic import Field


class RedisDSL(BaseSettings):
    host: str = Field(..., validation_alias='REDIS_HOST')
    port: int = Field(default=6379, validation_alias='REDIS_PORT')
    password: str = Field(..., validation_alias='REDIS_PASSWORD')
    db: int = Field(default=0, validation_alias='REDIS_DB')


class ElasticDSL(BaseSettings):
    es_host: str = Field(..., validation_alias='ES_HOST')
    es_port: int = Field(default=9200, validation_alias='ES_PORT')
    es_security: bool = Field(..., validation_alias='ES_SECURITY')


class PostgresDSL(BaseSettings):
    host: str = Field(..., validation_alias='SQL_HOST')
    port: int = Field(default=5432, validation_alias='SQL_PORT')
    dbname: str = Field(..., validation_alias='POSTGRES_DB')
    user: str = Field(..., validation_alias='POSTGRES_USER')
    password: str = Field(..., validation_alias='POSTGRES_PASSWORD')


class ETLSettings(BaseSettings):
    batch_size: int = Field(default=100, validation_alias='ETL_BATCH_SIZE')
    iteration_sleep: int = Field(default=5, validation_alias='ETL_ITERATION_SLEEP')
    es_index: str = Field(..., validation_alias='ETL_ES_INDEX')
