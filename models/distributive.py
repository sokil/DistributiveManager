from mongokit import Document
from bson.objectid import ObjectId


class Distributive(Document):
    __database__ = 'dl'
    __collection__ = 'distributives'

    structure = {
        'version': str,
        'environment': str,
        'url': str
    }