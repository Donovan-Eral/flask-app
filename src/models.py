from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from jwt import encode, decode
from datetime import datetime, timedelta
from flask import current_app
from src import login_manager, db


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')


    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0


    def __repr__(self):
        return "<Role %r>" % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128), unique=False)
    bio = db.Column(db.String(120), unique=False, nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, default=False)


    # ---------------------- PASSWORD HASHING FUNCTIONS ---------------------- #
    # These functions are used to make sure that the password is secure and 
    # accessing the non-hashed password is not possible.


    # Resricts the user from accessing the un-hashed password.
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')


    # Takes in the user's password and generates a hash for it.
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    # Checks if the password is correct.
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    # --------------------- EMAIL CONFIRMATION FUNCTIONS --------------------- #
    # These functions are used to make sure that the user is confirmed before
    # they can access the secure pages.


    # Generate a token with the default experation time of one hour.
    def generate_confirmation_token(self, expiration=3600):
        token = encode(
            {
                'confirm': self.id,
                'exp': datetime.utcnow() + timedelta(seconds=expiration)
            }, 
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        return token
    

    # Checks if the token is valid and if it is the user's confirmed attribute
    # is set to True.
    def confirm(self, token):
        try:
            data = decode(token, current_app.config['SECRET_KEY'], 
                algorithms=['HS256'])
        except:
            return False
        # Checks to make sure the id from the token matches the logged-in user
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    # --------------------------- OTHER FUNCTIONS ---------------------------- #

    def __repr__(self):
        return "<User %r>" % self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))