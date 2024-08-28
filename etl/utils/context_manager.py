from contextlib import contextmanager

from utils.db_connections import get_redis_conn, get_pg_conn, get_es_conn
from utils.logger import logger
from storage.redis_storage import RedisStorage

@contextmanager
def get_connections():
    logger.info('Getting connections')

    pg_conn = get_pg_conn()
    redis_conn = get_redis_conn()
    es_conn = get_es_conn()

    yield pg_conn, es_conn, RedisStorage(redis_conn)

    logger.info('Closing connections')

    pg_conn.close()
    redis_conn.close()
    es_conn.close()

    logger.info('Connections closed')
