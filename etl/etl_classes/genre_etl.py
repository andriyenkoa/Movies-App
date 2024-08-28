from .base_etl import BaseEtl


class GenreETL(BaseEtl):
    def __init__(self, pg_conn, es_conn, state_storage):
        super().__init__(pg_conn, es_conn, state_storage, 'last_modified_genre')

    @property
    def table(self):
        return f"{self.scheme}.genre"

    def get_modified_movies_ids_query(self, ids):
        placeholders = ', '.join(['%s'] * len(ids))
        query = f"""
            SELECT fw.id, fw.modified
            FROM content.film_work fw
            LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
            WHERE gfw.genre_id IN ({placeholders})
            ORDER BY fw.modified
        """
        yield from self.execute_sql(query, ids)