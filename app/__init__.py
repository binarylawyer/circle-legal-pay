"""
Flask Application Factory
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name='default'):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    # Register blueprints
    from app.views.main_views import main_blueprint
    from app.views.legal_views import legal_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(legal_blueprint, url_prefix='/legal')

    return app
