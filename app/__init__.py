from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__)

    from .routes.routes import query_bp
    app.register_blueprint(query_bp)


    return app