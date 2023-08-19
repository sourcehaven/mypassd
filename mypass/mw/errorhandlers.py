from flask import Flask

from mypass.exceptions import AuthException, WrongPasswordException


def base_error_handler(err: Exception):
    return {'msg': f'{err.__class__.__name__} :: {err}'}, 500


def auth_error_handler(err: AuthException):
    return {'msg': f'AUTHORIZATION FAILURE'}, 401


def wrong_password_error_handler(err: WrongPasswordException):
    return {'msg': f'AUTHORIZATION FAILURE :: Could not log in user -> cause: wrong username or password'}, 401


def register_error_handlers(app: Flask):
    app.register_error_handler(Exception, base_error_handler)
    app.register_error_handler(AuthException, auth_error_handler)
    app.register_error_handler(WrongPasswordException, wrong_password_error_handler)
