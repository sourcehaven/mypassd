from datetime import datetime

from flask import Blueprint, request, make_response
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt, \
    decode_token
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
def login():
    request_json = request.json
    ref_token = request_json.pop('refresh_token', None)
    username = request_json['username']
    password = request_json['password']
    user = db_utils.get_user_login(username=username, password=password)
    user = user.unlock(password)
    token = user.token
    uid = user.id
    identity = {IDENTITY_UID: uid, IDENTITY_USER: username, IDENTITY_PW: password, IDENTITY_TOK: token}
    logger.debug(f'Logging in with identity:\n    {identity["username"]}')
    # already logged-in users can request new fresh tokens
    # while also invalidating their old refresh tokens
    if ref_token is not None:
        # noinspection PyBroadException
        try:
            ref_jwt = decode_token(ref_token)
            ref_jti = ref_jwt['jti']
            ref_exp_dt = datetime.fromtimestamp(ref_jwt['exp'])
            db_utils.revoke_token(jti=ref_jti, exp_dt=ref_exp_dt)
            logger.debug(f'Revoked token with id: {ref_jti}')
        # invalid token error
        except Exception:
            pass
    access_token = create_access_token(identity=identity, fresh=True)
    refresh_token = create_refresh_token(identity=identity)
    tokens = {'access_token': access_token, 'refresh_token': refresh_token}
    resp = make_response(tokens, 201)
    resp.set_cookie('username', user.username or '')
    resp.set_cookie('email', user.email or '')
    resp.set_cookie('firstname', user.firstname or '')
    resp.set_cookie('lastname', user.lastname or '')
    return resp


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
        acc_jwt = get_jwt()
        acc_jti = acc_jwt['jti']
        acc_exp_dt = datetime.fromtimestamp(acc_jwt['exp'])
        ref_jwt = decode_token(request.json['refresh_token'])
        ref_jti = ref_jwt['jti']
        ref_exp_dt = datetime.fromtimestamp(ref_jwt['exp'])
        db_utils.revoke_tokens(acc_jti=acc_jti, ref_jti=ref_jti, acc_exp_dt=acc_exp_dt, ref_exp_dt=ref_exp_dt)
        logger.debug(f'Tokens: {acc_jti}, {ref_jti} has been successfully blacklisted.')
        return '', 204
    except KeyError:
        return '', 409
