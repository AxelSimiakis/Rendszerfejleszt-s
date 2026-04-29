from config import Config
from app.extensions import db
from apiflask import APIFlask
from flask_migrate import Migrate

migrate = Migrate()

def create_app(config_class=Config):
    app = APIFlask(__name__, 
                   title="JegyMester API", 
                   docs_path="/swagger")
    app.config.from_object(config_class)

    
    db.init_app(app)

    from flask_migrate import Migrate
    migrate=Migrate(app, db,render_as_batch=True)

    from app.blueprints import bp as main_bp
    app.register_blueprint(main_bp, url_prefix="/api")

    return app