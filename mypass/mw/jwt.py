# noinspection PyUnusedLocal
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    raise NotImplementedError()
    jti = jwt_payload['jti']
    return jti in blacklist
