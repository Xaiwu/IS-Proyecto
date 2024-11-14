from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from DataBase.DataBase import crear_database

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        from .routes import bp as main_bp
        app.register_blueprint(main_bp)
        db.create_all()

        # Llama a crear_database para asegurarte de que las tablas se crean
        crear_database()

    return app


__all__ = ['create_app', 'db']
