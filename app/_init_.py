# app/__init__.py

from flask import Flask
from .utils import init_db

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'
    
    # Initialize the database
    init_db()
    
    # Register routes
    from . import routes
    app.register_blueprint(routes.bp)

    return app
