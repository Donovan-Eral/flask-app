from flask import Flask

from .extensions import db
from .routes.user import user


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)
    app.register_blueprint(user)
    return app