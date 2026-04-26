from config import Config
from app.extensions import db, auth
from apiflask import APIFlask
from flask_migrate import Migrate
from authlib.jose import jwt
from flask import current_app

migrate = Migrate()

@auth.verify_token
def verify_token(token):
    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'])
        return data
    except Exception:
        return None

def create_app(config_class=Config):
    app = APIFlask(__name__, 
                   title="JegyMester API", 
                   docs_path="/swagger")
    
    app.config.from_object(config_class)

    
    db.init_app(app)
    migrate.init_app(app, db)

    from app.blueprints.user.routes import bp as user_bp
    from app.blueprints.movies.routes import bp as movie_bp
    from app.blueprints.screenings.routes import bp as screening_bp
    from app.blueprints.rooms.routes import bp as room_bp
    from app.blueprints.tickets.routes import bp as tickets_bp
    from app.blueprints.seat.routes import bp as seat_bp
    from app.blueprints.transactions.routes import bp as transaction_bp
    from app.blueprints.roles.routes import bp as role_bp
    


    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(movie_bp, url_prefix='/api/movies')
    app.register_blueprint(screening_bp, url_prefix='/api/screenings')
    app.register_blueprint(room_bp, url_prefix='/api/rooms')
    app.register_blueprint(tickets_bp, url_prefix='/api/tickets')
    app.register_blueprint(seat_bp, url_prefix='/api/seats')
    app.register_blueprint(transaction_bp, url_prefix='/api/transactions')
    app.register_blueprint(role_bp, url_prefix='/api/roles')
    return app