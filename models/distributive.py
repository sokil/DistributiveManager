from mongokit import Document
import re

def version_validator(version):
    regex = re.compile(r'^[0-9]+(?:\.[0-9]+(?:\.[0-9]+(?:-[0-9a-zA-Z\-\.]+)?)?)?$', re.IGNORECASE);
    return bool(regex.match(version))


class Distributive(Document):
    __database__ = 'dl'
    __collection__ = 'distributives'

    structure = {
        'version': str,
        'environment': str,
        'url': str
    }

    validators = {
        'version': version_validator
    }