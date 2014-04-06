from mongokit import Document


class Environment(Document):
    __database__ = 'dl'
    __collection__ = 'environment'

    structure = {
        'name': unicode
    }

    default_values = {
        'name': ''
    }