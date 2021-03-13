import asyncio

from flask import request, jsonify, make_response
from flask.views import View
from inject import attr

from core.services import Service


# Auth blueprint
class CreateUserView(View):
    service: Service = attr(Service)

    def dispatch_request(self):
        data = request.json

        username = data.get('username')
        nickname = data.get('nickname')
        password = data.get('password')

        if not username:
            return jsonify('Username is required'), 400

        if not nickname:
            return jsonify('Nickname is required'), 400

        if not password:
            return jsonify('Password is required'), 400

        try:
            created_user = self.service.register(
                username=username,
                nickname=nickname,
                password=password
            )

            return jsonify(created_user), 200
        except BaseException as error:
            return jsonify(str(error)), 400


class AuthorizeUserView(View):
    service: Service = attr(Service)

    def dispatch_request(self):
        data = request.json

        login = data.get('login')
        password = data.get('password')

        if not login:
            return jsonify('Login is required'), 400

        if not password:
            return jsonify('Password is required'), 400

        try:
            token = self.service.authorize(
                login=login,
                password=password
            )

            response = make_response(jsonify({'ok': True}), 200)
            response.set_cookie('token', token)

            return response
        except BaseException as error:
            return jsonify(str(error)), 401


class AuthenticateUserView(View):
    service: Service = attr(Service)

    def dispatch_request(self):
        token = request.cookies.get('token')

        if not token:
            return jsonify('No token'), 401

        try:
            user = self.service.authenticate(token)

            return jsonify(user), 200
        except BaseException as error:
            return jsonify(str(error)), 401


class LogoutUserView(View):
    service: Service = attr(Service)

    def dispatch_request(self):
        response = make_response(jsonify({'ok': True}), 200)
        response.set_cookie('token', '')

        return response


# Telegram blueprint
class TelegramAuthorizeUserView(View):
    service: Service = attr(Service)

    def dispatch_request(self):
        data = request.json

        phone_number = data.get('phone_number')
        password = data.get('password')
        code = data.get('code')

        if not phone_number:
            return jsonify('Phone number is required'), 400

        if not password:
            return jsonify('Password is required'), 400

        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            user = loop.run_until_complete(
                self.service.telegram_authorize_user(
                    phone_number,
                    password,
                    code
                )
            )

            return jsonify(user), 200
        except BaseException as error:
            return jsonify(str(error)), 449


class TelegramGetUserDialogsView(View):
    service: Service = attr(Service)

    def dispatch_request(self):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            dialogs = loop.run_until_complete(
                self.service.get_user_dialogs()
            )

            return jsonify(dialogs), 200
        except BaseException as error:
            return jsonify(str(error)), 400

