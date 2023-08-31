import os

from flask import Flask
from flask_jwt_extended import JWTManager

from mypass.db import db, migrate
from mypass.models.seri import ModelPlusJSONProvider
from mypass.mw import register_error_handlers, register_blueprints, check_if_token_in_blacklist
from mypass import config


def create_app():
    app = Flask(__name__)
    app.config.from_object(getattr(config, f'{os.environ.get("FLASK_ENV", "")}Config'))
    app.json = ModelPlusJSONProvider(app)

    register_blueprints(app)
    register_error_handlers(app)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    jwt = JWTManager(app)
    jwt.token_in_blocklist_loader(check_if_token_in_blacklist)

    if os.getenv('MYPASS_TESTENV', False):
        from ._dummy import init_db
        with app.app_context():
            init_db(db)

    return app
