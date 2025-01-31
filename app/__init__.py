from flask import Flask

def create_app():
    app = Flask(__name__)

    # Import and register blueprints/routes
    from .routes import api
    app.register_blueprint(api, url_prefix='/')

    return app
