from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = '19f4c4b47c8e726dec271f44'
db = SQLAlchemy(app)
api = Api(app)

from api import routes
