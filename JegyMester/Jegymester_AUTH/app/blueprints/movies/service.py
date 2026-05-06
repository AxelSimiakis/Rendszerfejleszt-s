from app.extensions import db
from app.models.movie import Movie
from sqlalchemy import select
from .schemas import MovieResponseSchema

class MovieService:
    @staticmethod
    def get_all_movies():
        movies = db.session.execute(select(Movie)).scalars().all()
        return MovieResponseSchema(many=True).dump(movies)

    @staticmethod
    def create_movie(data):
        try:
            movie = Movie(**data)
            db.session.add(movie)
            db.session.commit()
            return True, MovieResponseSchema().dump(movie)
        except Exception as ex:
            print(f"Error: {ex}")
            db.session.rollback()
            return False, "Failed to create movie"

    @staticmethod
    def update_movie(movie_id, data):
        try:
            
            movie = db.session.get(Movie, movie_id)
            if not movie:
                return False, "Movie not found"

            
            movie.title = data.get('title', movie.title)
            movie.description = data.get('description', movie.description)
            movie.duration_minutes = data.get('duration_minutes', movie.duration_minutes)

            db.session.commit()
            return True, MovieResponseSchema().dump(movie)
        except Exception as ex:
            print(f"Update Error: {ex}")
            db.session.rollback()
            return False, str(ex)

    @staticmethod
    def delete_movie(movie_id):
        try:
            movie = db.session.get(Movie, movie_id)
            if not movie:
                return False, "Movie not found"

            db.session.delete(movie)
            db.session.commit()
            return True, "Movie deleted successfully"
        except Exception as ex:
            print(f"Delete Error: {ex}")
            db.session.rollback()
            return False, str(ex)