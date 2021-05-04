from flask import request
from flask_restful import Resource, fields, marshal_with, abort
from sqlalchemy import exc

from api import db
from api.models import User

user_fields = {
    'user_id': fields.Integer,
    'username': fields.String,
    'email': fields.String
}


class UserResource(Resource):

    @marshal_with(user_fields)
    def get(self, user_id):
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            abort(404, message=f"User {user_id} doesn't exist")
        return user

    @marshal_with(user_fields)
    def put(self, user_id):
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            abort(404, message=f"User {user_id} doesn't exist")
        json_data = request.get_json(force=True)
        user.username = json_data['username']
        user.email = json_data['email']
        db.session.add(user)
        db.session.commit()
        return user

    @marshal_with(user_fields)
    def delete(self, user_id):
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            abort(404, message=f"User {user_id} doesn't exist")
        db.session.delete(user)
        db.session.commit()
        return user


class UserListResource(Resource):

    @marshal_with(user_fields)
    def get(self):
        users_list = User.query.all()
        return users_list

    @marshal_with(user_fields)
    def post(self):
        json_data = request.get_json(force=True)
        user = User(username=json_data['username'], email=json_data['email'])
        try:
            db.session.add(user)
            db.session.commit()
        except exc.IntegrityError:
            abort(409, message=f"Username '{user.username}' already exists!")
        user = User.query.filter_by(username=user.username).first()
        return user
