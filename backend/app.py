from flask import Flask
from flask_cors import CORS
from backend.db import db, ma, bcrypt
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SPECIAL_STAFF_CODE = os.getenv("SPECIAL_STAFF_CODE", "SECRET123")


def create_app():
    # Инициализация приложения внутри функции create_app
    app = Flask(__name__)

    # Основные настройки приложения
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'railway.db')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    # Инициализация расширений
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    JWTManager(app)
    CORS(app)

    from backend.routes import register_blueprints
    register_blueprints(app)

    return app


# Точка входа
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
