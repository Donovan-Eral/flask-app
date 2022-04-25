from flask import Flask
from app.extensions import db
from app.routes.user import user


app = Flask(__name__)
app.config.from_object('app.config.Config')
db.init_app(app)
app.register_blueprint(user)
# db.create_all(
