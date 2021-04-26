from api import api
from api.resources import UserListResource, UserResource

api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/user/<user_id>')
