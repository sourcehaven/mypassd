from flask import Flask


def base_error_handler(err: Exception):
    return {'msg': f'{err.__class__.__name__} :: {err}'}, 500


def register_error_handlers(app: Flask):
    app.register_error_handler(Exception, base_error_handler)
