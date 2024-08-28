from uuid import UUID
from typing import List
from pydantic import BaseModel


class Person(BaseModel):
    id: UUID
    name: str


class Genre(BaseModel):
    id: UUID
    name: str
    description: str


class FilmWork(BaseModel):
    id: UUID
    title: str
    description: str
    imdb_rating: float
    genres: List[str]
    actors: List[Person]
    writers: List[Person]
    directors: List[Person]
    actors_names: List[str]
    writers_names: List[str]
    directors_names: List[str]


    @classmethod
    def transform(cls, **film_data):
        def group_by(role, **data):
            return [
                Person(id=person.get("person_id"), name=person.get("person_name"))
                for person in data.get('persons') if person.get('person_role') == role
            ]

        actors = group_by('actor', **film_data)
        writers = group_by('writer', **film_data)
        directors = group_by('director', **film_data)

        return cls(
            id=film_data.get('id'),
            imdb_rating=film_data.get('rating') if film_data.get('rating') else 0.0,
            genres=film_data.get('genres'),
            title=film_data.get('title'),
            description=film_data.get('description'),
            actors=actors,
            writers=writers,
            directors=directors,
            actors_names=[actor.name for actor in actors],
            writers_names=[writer.name for writer in writers],
            directors_names=[director.name for director in directors],
        )



