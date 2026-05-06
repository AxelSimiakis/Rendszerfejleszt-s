from config import Config
from app.extensions import db
from apiflask import APIFlask
from flask_migrate import Migrate
from flask_cors import CORS

migrate = Migrate()

def create_app(config_class=Config):
    app = APIFlask(__name__, title="JegyMester API", docs_path="/swagger")
    app.config.from_object(config_class)
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    db.init_app(app)
    migrate.init_app(app, db)

    # Fontos: ez regisztrálja a token ellenőrzést és a role_required dekorátort is.
    import importlib
    importlib.import_module("app.blueprints")

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

    @app.get('/api/health')
    def health():
        return {'status': 'ok'}

    return app
