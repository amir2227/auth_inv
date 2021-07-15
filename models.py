from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    user_name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    email = db.Column(db.String(50), unique=True)
    role = db.Column(db.String(20))


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))


