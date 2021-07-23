from sqlalchemy.orm import backref
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(80), unique=True)
    user_name = db.Column(db.String(50))
    password = db.Column(db.String(256))
    email = db.Column(db.String(50), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    users = db.relationship('User', backref='role')

'''
db.create_all()
role = Role(id=1, name='OWNER')
role1 = Role(id=2, name='ADMIN')
role2 = Role(id=3, name='USER')
role3 = Role(id=4, name='PROUSER')
roles = [role, role1, role2, role3]
db.session.add_all(roles)
db.session.commit()
'''
