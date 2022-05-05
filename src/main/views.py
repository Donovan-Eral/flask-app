from flask import render_template
from src.main import main


# GET: Display the login form.
# POST: NEEED TO FILL IN
@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')