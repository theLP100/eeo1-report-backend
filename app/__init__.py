from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
import os
import psycopg2

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # #putting this in for heroku?
    # DATABASE_URL = os.environ['DATABASE_URL']
    # conn = psycopg2.connect(DATABASE_URL, sslmode = 'require')

    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
        app.config['SQLALCHEMY_ECHO']=True
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")

    from app.models.Eeo1_data import Eeo1_data
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from .routes.query import query_bp
    app.register_blueprint(query_bp)
    from .routes.adv_query import adv_query_bp
    app.register_blueprint(adv_query_bp)


    return app