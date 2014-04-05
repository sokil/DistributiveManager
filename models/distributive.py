from mongokit import Document
from bson.objectid import ObjectId


class Distributive(Document):
    __database__ = 'dl'
    __collection__ = 'distributive'

    structure = {
        'version': str,
        'env': ObjectId,
        'url': str
    }