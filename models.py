from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    user_name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    email = db.Column(db.String(50))
    role = db.Column(db.String(20))
