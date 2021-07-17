from flask import Flask
from flask_restful import Api

from resource.user import User, UserList

app = Flask(__name__)
api = Api(app)

user_list = []  # mysql

api.add_resource(User, '/api/v1/user/<string:username>')
api.add_resource(UserList, '/api/v1/users')

if __name__ == '__main__':
    app.run()