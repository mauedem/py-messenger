from flask import request, jsonify
from flask.views import View
from inject import attr

from core.services import Service


# Auth views
class RegisterUserView(View):
    service: Service = attr(Service)

    def dispatch_request(self):
        data = request.json

        username = data.get('username')
        nickname = data.get('nickname')
        password = data.get('password')

        if not username:
            return 'Username is required', 400

        if not nickname:
            return 'Nickname is required', 400

        if not password:
            return 'Password is required', 400

        try:
            created_user = self.service.register(
                username=username,
                nickname=nickname,
                password=password
            )

            return jsonify(created_user), 200
        except BaseException as error:
            return str(error), 400


class AuthorizeUserView(View):
    service: Service = attr(Service)

    def dispatch_request(self):
        data = request.json

        login = data.get('login')
        password = data.get('password')

        if not login:
            return 'Username is required', 400

        if not password:
            return 'Password is required', 400

        try:
            token = self.service.authorize(
                login=login,
                password=password
            )

            return jsonify({'token':  token}), 200
        except BaseException as error:
            return str(error), 401
