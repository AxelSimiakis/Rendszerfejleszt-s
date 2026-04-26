from apiflask import APIBlueprint

bp = APIBlueprint('screening', __name__, tag='screening')

from . import routes