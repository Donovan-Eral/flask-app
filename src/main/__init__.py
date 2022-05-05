from flask import Blueprint

main = Blueprint('main', __name__)

from src.main import views, errors