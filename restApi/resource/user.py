from flask_restful import Resource, reqparse
from restApi.model.user import User as UserModel
from restApi import db
from flask import jsonify, request
import json


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
    parser.add_argument('email', required=True, help='{error_msg')

    def get(self, username):
        '''Get user detail info.'''
        user = db.session.query(UserModel).filter(
            UserModel.username == username).first()
        if user:
            return user.as_dict()
        return {'message': 'user not found'}, 404

    def post(self, username):
        '''Create a user with password and email.'''
        data = User.parser.parse_args()
        user = db.session.query(UserModel).filter(
            UserModel.username == username).first()
        if user:
            return {'message': 'user already exist'}, 202
        user = UserModel(username=username,
                         password_hash=data['password'],
                         email=data['email'])
        db.session.add(user)
        db.session.commit()
        return user.as_dict(), 201

    def delete(self, username):
        '''Delete a user'''
        user = db.session.query(UserModel).filter(
            UserModel.username == username).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'Delete Success'}
        return {'message': 'user not found'}, 204

    def put(self, username):
        '''Update a user's info'''
        user = db.session.query(UserModel).filter(
            UserModel.username == username).first()
        if user:
            userInfo = request.get_json()
            print(userInfo)
            print(type(userInfo))
            if 'password' in userInfo and 'email' in userInfo:
                user.password_hash = userInfo['password']
                user.email = userInfo['email']
                db.session.commit()
            elif 'password' in userInfo:
                user.password_hash = userInfo['password']
                db.session.commit()
            else:
                user.email = userInfo['email']
                db.session.commit()
            return {'message': "Update user's info success"}, 201
        else:
            return {'message': 'User not found'}, 204


class UserList(Resource):
    def get(self):
        users = db.session.query(UserModel).all()
        return [u.as_dict() for u in users]
