import flask
from flask import Blueprint, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from flask_sqlalchemy import SQLAlchemy
from loguru import logger

from mypass.db import utils as db_utils
from mypass.models import User

AuthApi = Blueprint('auth', __name__)


@AuthApi.route('/api/auth/registration', methods=['POST'])
def registration():
    req = request.json
    username = req['username']
    password = req['password']
    email = req.get('email')
    forename = req.get('forename')
    surename = req.get('surename')
    db: SQLAlchemy = flask.current_app.extensions['sqlalchemy']
    user = User.create(username=username, password=password, forename=forename, surename=surename, email=email)
    db.session.add(user)
    db.session.commit()
    return flask.redirect(flask.url_for('auth.login', _method='POST', token=user.token), 307)


@AuthApi.route('/api/auth/login', methods=['POST'])
def login():
    request_json = request.json
    request_args = request.args
    username = request_json['username']
    password = request_json['password']
    token = request_args.get(
        'token', db_utils.get_user_login(username=username, password=password).unlock(password).token)
    identity = {'username': username, 'password': password, 'token': token}
    logger.debug(f'Logging in with identity:\n    {identity["username"]}')
    access_token = create_access_token(identity=identity, fresh=True)
    refresh_token = create_refresh_token(identity=identity)
    return {'access_token': access_token, 'refresh_token': refresh_token}, 201


@AuthApi.route('/api/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=False)
    return {
        'access_token': access_token
    }, 201


@AuthApi.route('/api/auth/logout', methods=['DELETE'])
@jwt_required(optional=True)
def logout():
    logger.debug('Logging out user.')
    try:
        jti = get_jwt()['jti']
        logger.debug(f'Blacklisting token: {jti}.')
        # blacklisting token ... --> blacklist.add(jti)
        return '', 204
    except KeyError:
        return '', 409
