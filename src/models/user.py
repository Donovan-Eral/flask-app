from src.extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120), unique=False)
    bio = db.Column(db.String(120), unique=False, nullable=True)
    role = db.Column(db.String(80), unique=False)

    def __repr__(self):
        return "<User %r>" % self.username