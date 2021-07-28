from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('password', type=str, required=True)


    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400
        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created success"}, 201

class UserList(Resource):
    @jwt_required()
    def get(self):
        return {"users":[user.json() for user in UserModel.query.all()]}