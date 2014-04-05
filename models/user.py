from mongokit import Document


class User(Document):
    __database__ = 'dl'
    __collection__ = 'users'

    structure = {
        'email': str,
        'password': str,
    }


    def is_authenticated(self):
        return True


    def is_active(self):
        return True


    def is_anonymous(self):
        return False


    def get_id(self):
        return self['email']


    def has_password(self, password):
        return password == self['password']
