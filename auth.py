from flask import jsonify, request, make_response
from models import User
import jwt
import uuid
import datetime
from app import app, db
from werkzeug.security import generate_password_hash, check_password_hash


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


@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    print(f'this is user-----> {user}')
    print(f'this is not user-----> {not user}')
    if not not user:
        return make_response('You signup befor', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), user_name=data['user_name'], password=hashed_password, email=data['email'], role='user')
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!'})
