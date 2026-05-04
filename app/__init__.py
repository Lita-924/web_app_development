from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    # Register blueprints safely
    from app.routes.recipe import recipe_bp
    from app.routes.search import search_bp
    from app.routes.category import category_bp
    from app.routes.share import share_bp

    app.register_blueprint(recipe_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(share_bp)

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
