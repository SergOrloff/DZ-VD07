from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from app.routes import main

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    from app.routes import main
    app.register_blueprint(main)

    return app