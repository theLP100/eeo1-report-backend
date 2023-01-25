from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

db = SQLAlchemy()
migrate = Migrate()
load_dotenv

def create_app(test_config=None):
    app = Flask(__name__)

    from app.models.Eeo1_data_line import Eeo1_data_line
    
    db.init_app(app)
    
    from .routes.routes import query_bp
    app.register_blueprint(query_bp)


    return app