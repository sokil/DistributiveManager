from mongokit import Document


class Apikey(Document):

    __database__ = 'dl'
    __collection__ = 'apikeys'

    structure = {
        'name': unicode,
        'key': unicode
    }

    default_values = {
        'name': '',
        'key': ''
    }

    @staticmethod
    def generate_key():
        import random
        alphabet = u'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
        return ''.join([random.choice(alphabet) for _ in range(40)])

    def regenerate_key(self):
        self['key'] = self.generate_key()
        self.save()

    def save(self, uuid=False, validate=None, safe=True, *args, **kwargs):

        # before save
        if not self['key']:
            self['key'] = self.generate_key()

        # save
        Document.save(self, uuid, validate, safe, *args, **kwargs)