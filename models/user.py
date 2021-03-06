from mongokit import Document
from random import randint
from crypt import crypt


class User(Document):
    __database__ = 'dl'
    __collection__ = 'users'

    structure = {
        'email': unicode,
        'password': unicode,
        'salt': unicode
    }

    default_values = {
        'email': ''
    }

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self['email']

    def set_password(self, password):
        # generate salt
        salt = u''
        alphabet = u'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890!@#$%^&*()'
        alphabet_length = len(alphabet) - 1
        for i in range(0, 10):
            salt += alphabet[randint(0, alphabet_length)]

        # store password and salt
        self['password'] = self.get_password_hash(password, salt)
        self['salt'] = salt

        return self

    @staticmethod
    def get_password_hash(password, salt):
        return unicode(crypt(password, salt))

    def has_password(self, password):
        return self.get_password_hash(password, self['salt']) == self['password']
