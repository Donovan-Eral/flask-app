# from os import environ
# from flask import Blueprint, jsonify, request
# import uuid
# from werkzeug.security import generate_password_hash, check_password_hash
# import jwt
# import datetime
# from functools import wraps

# from app import db
# from app.models.user import User
# from app.permissions import PERMISSIONS

# user = Blueprint('user', __name__, url_prefix='/user')


# def valid_token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None

#         # change this to the authentication section on postman
#         if 'x-access-token' in request.headers:
#             token = request.headers['x-access-token']

#         if not token:
#             return jsonify({'message': 'Token is missing!'}), 401

#         try:
#             data = jwt.decode(token, 'secret', algorithms=['HS256'])
#             current_user = User.query.filter_by(
#                 public_id=data['public_id']).first()
#         except jwt.exceptions.InvalidTokenError:
#             return jsonify({'message': 'Token is invalid!'}), 401

#         # Check if user has permission to access the resource
#         if f.__name__ in PERMISSIONS[current_user.role]:
#             return f(current_user, *args, **kwargs)
#         else:
#             return jsonify({'message': 'Permission denied!'}), 401

#     return decorated


# # API root
# @user.route('/')
# def index():
#     return 'API USER ROOT'


# # -----------------------------------POST---------------------------------- #
# # Creating a new user from json input
# @user.route('/signup', methods=['POST'])
# def signup():
#     data = request.get_json()

#     hashed_password = generate_password_hash(data['password'], method='sha256')

#     new_user = User(
#         public_id=str(uuid.uuid4()),
#         username=data['username'],
#         email=data['email'],
#         password=hashed_password,
#         bio=data['bio'],
#         role='user'  # default role
#     )
#     db.session.add(new_user)
#     db.session.commit()

#     return {'message': 'User created successfully.'}, 201


# # -----------------------------------GET----------------------------------- #
# # Getting all users
# @user.route('/get_all', methods=['GET'])
# @valid_token_required
# def get_all(current_user):
#     users = User.query.all()
#     users_list = []
#     for user in users:
#         user_data = {
#             'public_id': user.public_id,
#             'username': user.username,
#             'email': user.email,
#             'bio': user.bio,
#             'role': user.role
#         }
#         users_list.append(user_data)
#     return jsonify({'users': users_list}), 200


# # Getting a user by their public id
# @user.route('/get_by_id/<public_id>', methods=['GET'])
# @valid_token_required
# def get_by_id(current_user, public_id):
#     user = User.query.filter_by(public_id=public_id).first()
#     if not user:
#         return jsonify({'message': 'No user found!'}), 404
#     user_data = {
#         'public_id': user.public_id,
#         'username': user.username,
#         'email': user.email,
#         'bio': user.bio,
#         'role': user.role
#     }
#     return jsonify({'user': user_data}), 200


# # Getting the current user
# @user.route('/get_self', methods=['GET'])
# @valid_token_required
# def get_self(current_user):
#     user_data = {
#         'public_id': current_user.public_id,
#         'username': current_user.username,
#         'email': current_user.email,
#         'bio': current_user.bio,
#         'role': current_user.role
#     }
#     return jsonify({'user': user_data}), 200


# # -----------------------------------PUT----------------------------------- #
# # Promotes a user to admin
# @user.route('/promote/<public_id>', methods=['PUT'])
# @valid_token_required
# def promote(current_user, public_id):
#     user = User.query.filter_by(public_id=public_id).first()
#     if not user:
#         return jsonify({'message': 'No user found!'}), 404
#     if user.role == 'user':
#         user.role = 'admin'
#     elif user.role == 'admin':
#         user.role = 'superadmin'
#     db.session.commit()

#     return jsonify({'message': 'User has been promoted!'}), 200


# @user.route('/demote/<public_id>', methods=['PUT'])
# @valid_token_required
# def demote(current_user, public_id):
#     user = User.query.filter_by(public_id=public_id).first()
#     if not user:
#         return jsonify({'message': 'No user found!'}), 404
#     if user.role == 'superadmin':
#         user.role = 'admin'
#     elif user.role == 'admin':
#         user.role = 'user'
#     db.session.commit()

#     return jsonify({'message': 'User has been demoted!'}), 200


# # -----------------------------------DELETE-------------------------------- #
# # Deleting a user by id
# @user.route('/delete_by_id/<public_id>', methods=['DELETE'])
# @valid_token_required
# def delete_by_id(current_user, public_id):
#     user = User.query.filter_by(public_id=public_id).first()
#     if not user:
#         return jsonify({'message': 'No user found!'}), 404
#     db.session.delete(user)
#     db.session.commit()

#     return jsonify({'message': 'User has been deleted!'}), 200


# # Delete this user
# @user.route('/delete_self', methods=['DELETE'])
# @valid_token_required
# def delete_self(current_user):
#     db.session.delete(current_user)
#     db.session.commit()

#     return jsonify({'message': 'User has been deleted!'}), 200


# # ----------------------------------LOGIN---------------------------------- #
# # Login a user
# @user.route('/login')
# def login():
#     auth = request.authorization

#     if not auth or not auth.username or not auth.password:
#         return jsonify({'message': 'Could not verify'}), 401

#     user = User.query.filter_by(username=auth.username).first()

#     if not user:
#         return jsonify({'message': 'Could not verify'}), 401

#     if check_password_hash(user.password, auth.password):
#         token = jwt.encode({
#             'public_id': user.public_id,
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
#         }, 'secret', algorithm='HS256')

#         return jsonify({'token': token}), 200

#     return jsonify({'message': 'Could not verify'}), 401
