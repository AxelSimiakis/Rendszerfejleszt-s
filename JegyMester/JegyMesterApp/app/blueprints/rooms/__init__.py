from apiflask import APIBlueprint

bp = APIBlueprint('room', __name__, tag="room")

from . import routes