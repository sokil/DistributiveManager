from flask import current_app, abort, request
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature


class TokenAuthGenerator():

    def __init__(self, expiration=1200):
        self.data = {}
        self.serializer = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)

    def set_data(self, data):
        self.data = data
        return self

    def get_token(self):
        return self.serializer.dumps(self.data)


class TokenAuthReader():

    def __init__(self):
        self.data_verifier_callback = None

    def get_data(self):
        if 'X-Auth-Token' in request.headers:
            token = request.headers['X-Auth-Token']
        elif 'auth_token' in request.args:
            token = request.args['auth_token']
        else:
            raise TokenNotSpecified

        s = Serializer(current_app.config['SECRET_KEY'])
        return s.loads(token)

    def data_verifier(self, function):
        self.data_verifier_callback = function
        return function

    def login_required(self, function):
        def wrapper(*args, **kwargs):
            try:
                data = self.get_data()
            except SignatureExpired:
                abort(403)
            except BadSignature:
                abort(403)
            except TokenNotSpecified:
                abort(400)

            if self.data_verifier_callback and not self.data_verifier_callback(data):
                abort(403)

            # execute function
            return function(*args, **kwargs)

        return wrapper


class TokenNotSpecified(Exception):
    """
    Token not found in header and query string
    """

