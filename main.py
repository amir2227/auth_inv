from app import app
from flask import jsonify, request
from functools import wraps
from models import User
import user_management, auth, config
import jwt

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


@app.route("/unpro")
def unpro():
    return jsonify({'message': 'unpro'})


@app.route("/pro")
@token_required
def pro():
    return jsonify({'message': 'pro'})


if __name__ == "__main__":
    app.run(debug=True)
