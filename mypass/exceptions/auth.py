class AuthException(RuntimeError):
    pass


class WrongPasswordException(AuthException):
    pass
