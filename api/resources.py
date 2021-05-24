from flask import request
from flask_restful import Resource, fields, marshal_with, abort
from sqlalchemy import exc

from api import db
from api.models import User, PersonalInfo, Address

info_field = {
    'first_name': fields.String,
    'last_name': fields.String,
    'birth_date': fields.String
}

address_field = {
    'address': fields.String,
    'city': fields.String,
    'state': fields.String,
    'country': fields.String,
    'postal_code': fields.String
}

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'infos': fields.Nested(info_field),
    'addresses': fields.Nested(address_field)
}


class UserResource(Resource):

    @marshal_with(user_fields)
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
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
        user = User.query.filter_by(id=user_id).first()
        address = Address.query.filter_by(user_id=user.id).first()
        info = PersonalInfo.query.filter_by(user_id=user.id).first()
        if not user:
            abort(404, message=f"User {user_id} doesn't exist")
        db.session.delete(user)
        db.session.delete(address)
        db.session.delete(info)
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
        print(json_data)
        personal_info = PersonalInfo(first_name=json_data['infos'][0]['first_name'],
                                     last_name=json_data['infos'][0]['last_name'],
                                     birth_date=json_data['infos'][0]['birth_date'],
                                     user_id=user.id)
        address = Address(address=json_data['addresses'][0]['address'],
                          city=json_data['addresses'][0]['city'],
                          state=json_data['addresses'][0]['state'],
                          country=json_data['addresses'][0]['country'],
                          postal_code=json_data['addresses'][0]['postal_code'],
                          user_id=user.id)
        db.session.add(personal_info)
        db.session.add(address)
        db.session.commit()
        return user
