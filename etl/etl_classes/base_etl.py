from abc import ABC, abstractmethod
from datetime import datetime

from elasticsearch.helpers import bulk

from utils.data_validation import FilmWork
from utils.logger import logger
from state_manager import State
from utils.connection_validation import ETLSettings


class BaseEtl(ABC):
    batch_size = ETLSettings().batch_size
    scheme = 'content'
    es_index = ETLSettings().es_index

    def __init__(self, pg_conn, es_conn, state_storage, last_modified_key):
        self.pg_conn = pg_conn
        self.es_conn = es_conn
        self.state = State(storage=state_storage)
        self.last_modified_key = last_modified_key

    @property
    @abstractmethod
    def table(self):
        pass

    def execute_sql(self, query, values):
        with self.pg_conn.cursor() as cursor:
            try:
                cursor.execute(query, values)

            except Exception as e:
                logger.error(e)
            while data := cursor.fetchmany(size=self.batch_size):
                yield data

    def last_modified_date(self):
        last_modified_date = self.state.get_state(self.last_modified_key)
        if last_modified_date:
            last_modified_date = datetime.fromisoformat(last_modified_date)
        else:
            last_modified_date = datetime.strptime('1970-01-01 00:00:00.000000', '%Y-%m-%d %H:%M:%S.%f')
        return last_modified_date

    def get_modified_ids(self):
        query = f"SELECT id, modified FROM {self.table} WHERE modified > %s ORDER BY modified"
        values = (self.last_modified_date(),)
        yield from self.execute_sql(query, values)

    def get_modified_movies_ids(self):
        for data in self.get_modified_ids():
            ids = tuple(row['id'] for row in data)
            yield from self.get_modified_movies_ids_query(ids)
            self.state.set_state(self.last_modified_key, data[-1]['modified'].isoformat())

    def extract(self):
        for data in self.get_modified_movies_ids():
            ids = tuple(row['id'] for row in data)
            placeholders = ', '.join(['%s'] * len(ids))
            query = f"""
                SELECT
                    fw.id, 
                    fw.title, 
                    COALESCE(fw.description, '') as description,
                    fw.rating, 
                    fw.type, 
                    fw.created, 
                    fw.modified, 
                    COALESCE (
                       json_agg(
                           DISTINCT jsonb_build_object(
                               'person_role', pfw.role,
                               'person_id', p.id,
                               'person_name', p.full_name
                           )
                       )
                       , '[]'
                    ) as persons,
                    json_agg(DISTINCT g.name) as genres
                FROM content.film_work fw
                LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
                LEFT JOIN content.person p ON p.id = pfw.person_id
                LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
                LEFT JOIN content.genre g ON g.id = gfw.genre_id
                WHERE fw.id IN ({placeholders})
                GROUP BY fw.id, fw.modified
                ORDER BY fw.modified;
            """
            yield from self.execute_sql(query, ids)

    def transform(self):
        validator = FilmWork
        for data in self.extract():
            documents = []
            for row in data:
                document = validator.transform(**row)

                documents.append(document)
            yield documents

    def load(self):
        for documents in self.transform():
            actions = [
                {
                    "_index": self.es_index,
                    "_id": str(doc.id),  # TODO: check if we can use doc.id,
                    "_source": doc.dict()
                }
                for doc in documents
            ]

            try:
                logger.info(f"Indexing {len(actions)} documents to {self.es_index} index from {self.table} table")
                bulk(self.es_conn, actions)
            except Exception as e:
                logger.error(e)
                raise


    @abstractmethod
    def get_modified_movies_ids_query(self, ids):
        pass
