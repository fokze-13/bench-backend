class InvalidTokenError(Exception):
    pass

class ExpiredTokenError(InvalidTokenError):
    pass
