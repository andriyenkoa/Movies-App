from elasticsearch import Elasticsearch, ConnectionError as esConnectionError
from elastic_transport import ConnectionTimeout as esConnectionTimeout
import psycopg
from psycopg.rows import dict_row
from psycopg.errors import OperationalError as pgOperationalError
from redis import Redis, ConnectionError as redisConnectionError, TimeoutError as redisTimeoutError

from .logger import logger
from .connection_validation import PostgresDSL, RedisDSL, ElasticDSL
from .backoff import backoff


@backoff(exceptions=(pgOperationalError,))
def get_pg_conn():
    dsl = PostgresDSL().dict()
    logger.info('Connecting to Postgres')

    return psycopg.connect(**dsl, row_factory=dict_row)


@backoff(exceptions=(redisTimeoutError, redisConnectionError,))
def get_redis_conn():
    dsl = RedisDSL().dict()
    logger.info('Connecting to Redis')

    return Redis(**dsl)


@backoff(exceptions=(esConnectionError, esConnectionTimeout,))
def get_es_conn():
    dsl = ElasticDSL().dict()
    logger.info('Connecting to Elasticsearch')

    return Elasticsearch(
        hosts=[{"host": dsl['es_host'], "port": dsl['es_port'], "scheme": "http"}],
    )
