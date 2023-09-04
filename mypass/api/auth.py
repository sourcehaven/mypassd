from flask import Blueprint, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from loguru import logger

from mypass.db import utils as db_utils
from .com import IDENTITY_UID, IDENTITY_USER, IDENTITY_PW, IDENTITY_TOK

AuthApi = Blueprint('auth', __name__)


@AuthApi.route('/api/auth/registration', methods=['POST'])
def registration():
    request_json = request.json
    user = db_utils.insert_user(**request_json)
    username = request_json['username']
    password = request_json['password']
    token = user.token
    uid = user.id
    identity = {IDENTITY_UID: uid, IDENTITY_USER: username, IDENTITY_PW: password, IDENTITY_TOK: token}
    logger.debug(f'Registering user with identity:\n    {identity["username"]}')
    access_token = create_access_token(identity=identity, fresh=True)
    refresh_token = create_refresh_token(identity=identity)
    tokens = {'access_token': access_token, 'refresh_token': refresh_token, 'token': token}
    return tokens, 201


@AuthApi.route('/api/auth/login', methods=['POST'])
@jwt_required(optional=True)
def login():
    request_json = request.json
    username = request_json['username']
    password = request_json['password']
    user = db_utils.get_user_login(username=username, password=password)
    user = user.unlock(password)
    token = user.token
    uid = user.id
    identity = {IDENTITY_UID: uid, IDENTITY_USER: username, IDENTITY_PW: password, IDENTITY_TOK: token}
    logger.debug(f'Logging in with identity:\n    {identity["username"]}')
    access_token = create_access_token(identity=identity, fresh=True)
    refresh_token = create_refresh_token(identity=identity)
    tokens = {'access_token': access_token, 'refresh_token': refresh_token}
    return tokens, 201


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
        db_utils.insert_blacklist_token(jti)
        logger.debug(f'Token: {jti} has been successfully blacklisted.')
        return '', 204
    except KeyError:
        return '', 409


@AuthApi.route('/api/auth/update', methods=['POST'])
@jwt_required(fresh=True)
def user_update():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=False)
    return {
        'access_token': access_token
    }, 201
