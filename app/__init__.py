from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()
load_dotenv

def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")

    from app.models.Eeo1_data_line import Eeo1_data_line
    
    db.init_app(app)
    
    from .routes.routes import query_bp
    app.register_blueprint(query_bp)


    return app