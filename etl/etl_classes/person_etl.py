from .base_etl import BaseEtl


class PersonETL(BaseEtl):
    def __init__(self, pg_conn, es_conn, state_storage):
        super().__init__(pg_conn, es_conn, state_storage, 'last_modified_person')

    @property
    def table(self):
        return f"{self.scheme}.person"

    def get_modified_movies_ids_query(self, ids):
        placeholders = ', '.join(['%s'] * len(ids))
        query = f"""
            SELECT fw.id, fw.modified
            FROM content.film_work fw
            LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
            WHERE pfw.person_id IN ({placeholders})
            ORDER BY fw.modified
        """
        yield from self.execute_sql(query, ids)
