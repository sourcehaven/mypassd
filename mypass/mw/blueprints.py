from flask import Flask

from mypass.api import AuthApi, VaultApi, TeapotApi


def register_blueprints(app: Flask):
    app.register_blueprint(AuthApi)
    app.register_blueprint(VaultApi)
    app.register_blueprint(TeapotApi)
