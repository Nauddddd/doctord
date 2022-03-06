from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()

def create_app():
    app = Flask(__name__,
    template_folder="templates",
    static_folder="templates/static")


    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True


    app.config['SECRET_KEY'] = '2b225155eb9153b0925d57727fdbd3ab70a6c202'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://duan:admin@localhost:5432/students'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app