from .base_etl import BaseEtl


class FilmWorkETL(BaseEtl):
    def __init__(self, pg_conn, es_conn, state_storage):
        super().__init__(pg_conn, es_conn, state_storage, 'last_modified_film_work')

    @property
    def table(self):
        return f"{self.scheme}.film_work"

    def get_modified_movies_ids_query(self, ids):
        yield [{"id": fw_id} for fw_id in ids]
