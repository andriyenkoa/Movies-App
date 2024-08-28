from psycopg import connection as pg_connection
from elasticsearch import Elasticsearch
from time import sleep

from etl_classes import PersonETL, GenreETL, FilmWorkETL
from storage.base_storage import BaseStorage
from utils.connection_validation import ETLSettings
from utils.context_manager import get_connections


def etl_pg_to_es(pg_conn: pg_connection, es_conn: Elasticsearch, storage: BaseStorage) -> None:
    etls = [PersonETL, GenreETL, FilmWorkETL]

    for etl in etls:
        etl(pg_conn, es_conn, storage).load()


if __name__ == "__main__":
    while True:
        with get_connections() as connections:
            etl_pg_to_es(*connections)
        sleep(ETLSettings().iteration_sleep)