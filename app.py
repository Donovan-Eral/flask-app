from flask import Flask
from src.extensions import db
from src.routes.user import user


app = Flask(__name__)
app.config.from_object('src.config.Config')
db.init_app(app)
app.register_blueprint(user)


@app.route('/')
def index():
    return 'Hello, World!'
