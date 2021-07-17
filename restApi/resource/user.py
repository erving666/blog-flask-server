from flask_restful import Resource, reqparse

user_list = []


def min_length_str(min_length):
    def validate(s):
        if s is None:
            raise Exception('pass required')
        if not isinstance(s, (int, str)):
            raise Exception('password format error')
        s = str(s)
        if len(s) >= min_length:
            return s
        raise Exception("String must be at least %i characters long" %
                        min_length)

    return validate


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('password',
                        type=min_length_str(5),
                        required=True,
                        help='{error_msg}')

    def get(self, username):
        '''Get user detail info.'''
        for user in user_list:
            if user['username'] == username:
                return user
        return {'message': 'user not found'}, 404

    def post(self, username):
        '''Create a user with a pass.'''

        data = User.parser.parse_args()
        for u in user_list:
            if u['username'] == username:
                return {'message': 'user existed'}, 202
        user = {
            'username': username,
            # 'password': request.get_json().get('password')
            'password': data.get('password')  # 非空判断如何实现？密码存储安全？
        }
        user_list.append(user)
        return user, 201

    def delete(self, username):
        '''Delete a user'''
        user_find = None
        for user in user_list:
            if user['username'] == username:
                user_find = user
        if user_find:
            user_list.remove(user_find)
            return user_find
        else:
            return {'message': 'user not found'}, 204

    def put(self, username):
        '''Update a user's info'''
        user_find = None
        for user in user_list:
            if user['username'] == username:
                user_find = user
        if user_find:
            data = User.parser.parse_args()
            user_list.remove(user_find)
            # user_find['password'] = request.get_json()['password']
            user_find['password'] = data.get('password')
            user_list.append(user_find)
            return user_find
        else:
            return {'message': 'user not found'}, 204


class UserList(Resource):
    def get(self):
        return user_list
