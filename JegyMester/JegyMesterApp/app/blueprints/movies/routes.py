from .service import MovieService
from .schemas import MovieRequestSchema, MovieResponseSchema
from apiflask import HTTPError
from app.blueprints.movies import bp

@bp.get('/')
@bp.output(MovieResponseSchema(many=True))
def get_movies():
    
    return MovieService.get_all_movies()

@bp.post('/')
@bp.input(MovieRequestSchema, location="json")
@bp.output(MovieResponseSchema)
def add_movie(json_data):
    
    success, response = MovieService.create_movie(json_data)
    if success:
        return response, 201
    raise HTTPError(message=response, status_code=400)

@bp.put('/<int:movie_id>')
@bp.input(MovieRequestSchema, location="json")
@bp.output(MovieResponseSchema)
def update_movie(movie_id, json_data):
   
    success, response = MovieService.update_movie(movie_id, json_data)
    if success:
        return response, 200
    
    
    status = 404 if response == "Movie not found" else 400
    raise HTTPError(message=response, status_code=status)

@bp.delete('/<int:movie_id>')
@bp.output({}, status_code=204)
def delete_movie(movie_id):
    
    success, response = MovieService.delete_movie(movie_id)
    if success:
        return ""
    raise HTTPError(message=response, status_code=404)