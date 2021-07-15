from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__, instance_relative_config=False)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://amir2227:5620027546@localhost:3306/test'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)
