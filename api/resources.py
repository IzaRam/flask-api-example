from flask_restful import Resource, fields, marshal_with, abort
from api.models import User

user_fields = {
    'user_id': fields.Integer,
    'username': fields.String,
    'email': fields.String
}


# TODO add methods POST PUT DELETE

class UserResource(Resource):

    @marshal_with(user_fields)
    def get(self, user_id):
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            abort(404, message=f"User {user_id} doesn't exist")
        return user


class UserListResource(Resource):

    @marshal_with(user_fields)
    def get(self):
        users_list = User.query.all()
        return users_list
