# app/blueprints/user/__init__.py
from apiflask import APIBlueprint

bp = APIBlueprint('user', __name__, tag="user")

from . import routes 