import sqlite3
from flask_restful import Resource ,reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',required=True,help="Username is required" , type=str)
    parser.add_argument('password',required=True,help="Password is required" , type=str)
    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message':'An item with name {} already exist.'.format(data['username'])} , 400
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        user = (data['username'], data['password'])
        insert_user = "INSERT INTO users VALUES( NULL, ? , ?)"
        cursor.execute(insert_user,user)
        connection.commit()
        connection.close()
        return {"message":"User created successfullt"},201




