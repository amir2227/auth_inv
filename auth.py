from flask import jsonify, request, make_response
from models import User
import jwt
import config, uuid
import datetime
from app import app, db
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

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


@app.route('/user', methods=['POST'])
@token_required
def create_user(current_user):
    if not current_user.admin != 'admin':
        return jsonify({'message' : 'Cannot perform that function!'})

    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), user_name=data['user_name'], password=hashed_password, email=data['email'], role='user')
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : 'New user created!'})


@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):

    if not current_user.role == 'user':
        return jsonify({'message' : 'Cannot perform that function!'})

    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['user_name'] = user.user_name
        user_data['password'] = user.password
        user_data['role'] = user.role
        user_data['email'] = user.email
        output.append(user_data)

    return jsonify({'users' : output})


@app.route('/login')
def login():
    
    passwrd = request.args['password']
    username = request.args['username']
    if not username or not passwrd:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(user_name=username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user.password, passwrd):
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)}, app.config['SECRET_KEY'])

        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
