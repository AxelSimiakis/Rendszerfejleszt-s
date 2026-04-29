from apiflask import APIBlueprint

bp = APIBlueprint('main', __name__, tag="main")

@bp.route('/')
def index():
    return 'This is The Main Blueprint'

from app.blueprints.user import bp as user_bp
bp.register_blueprint(user_bp, url_prefix="/user")
from app.blueprints.transactions import bp as transaction_bp
bp.register_blueprint(transaction_bp, url_prefix="/transactions")
from app.blueprints.tickets import bp as ticket_bp
bp.register_blueprint(ticket_bp, url_prefix="/tickets")
from app.blueprints.seat import bp as seat_bp
bp.register_blueprint(seat_bp, url_prefix="/seat")
from app.blueprints.screenings import bp as screening_bp
bp.register_blueprint(screening_bp, url_prefix="/screenings")
from app.blueprints.rooms import bp as room_bp
bp.register_blueprint(room_bp, url_prefix="/rooms")
from app.blueprints.roles import bp as role_bp
bp.register_blueprint(role_bp, url_prefix="/roles")
from app.blueprints.movies import bp as movie_bp
bp.register_blueprint(movie_bp, url_prefix="/movies")


from app.models import *