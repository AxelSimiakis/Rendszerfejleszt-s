from apiflask import APIBlueprint

bp = APIBlueprint('tickets', __name__, tag="tickets")

from . import routes