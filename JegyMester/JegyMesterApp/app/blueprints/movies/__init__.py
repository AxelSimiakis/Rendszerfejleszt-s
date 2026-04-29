from apiflask import APIBlueprint

bp = APIBlueprint('movie', __name__, tag="movie")

from . import routes