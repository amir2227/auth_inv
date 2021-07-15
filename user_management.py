from flask import request, jsonify
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from models import User, Role
import jwt, uuid
import config


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, config.SECRET_KEY)
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/create_user', methods=['POST'])
@token_required
def create_user(current_user):
    if not current_user.role_id != 1 or not current_user.role_id != 2:
        return jsonify({'message': 'Cannot perform that function!'})

    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), user_name=data['user_name'], password=hashed_password, email=data['email'], role='user')
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!'})


@app.route('/get_all_user', methods=['GET'])
@token_required
def get_all_users(current_user):

    if not current_user.role.name == 'OWNER' and not current_user.role.name == 'ADMIN':
        return jsonify({'message': 'Cannot perform that function!'})

    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['user_name'] = user.user_name
        user_data['password'] = user.password
        user_data['role'] = user.role.name
        user_data['email'] = user.email
        output.append(user_data)

    return jsonify({'users': output})


@app.route('/promote_user/<email>/<role_name>', methods=['PUT'])
@token_required
def promote_user(current_user, email, role_name):
    if not current_user.role.name == 'ADMIN' and not current_user.role.name == 'OWNER':
        return jsonify({'message': 'Cannot perform that function!'})

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'message': 'No user found!'})
    role = Role.query.filter_by(name=role_name)
    user.role = role
    db.session.commit()

    return jsonify({'message': 'The user has been promoted!'})
