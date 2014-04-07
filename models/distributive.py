import re
import os
from mongokit import Document
from bson.objectid import ObjectId
from models.environment import Environment
from flask import current_app, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage


def version_validator(version):
    regex = re.compile(r'^[0-9]+(?:\.[0-9]+(?:\.[0-9]+(?:-[0-9a-zA-Z\-\.]+)?)?)?$', re.IGNORECASE);
    return bool(regex.match(version))


class Distributive(Document):
    __database__ = 'dl'
    __collection__ = 'distributives'

    environment_instance = None

    structure = {
        'version': unicode,
        'environment': ObjectId,
        'file': unicode
    }

    default_values = {
        'version': '',
        'file': ''
    }

    validators = {
        'version': version_validator
    }

    def set_environment(self, environment):
        if type(environment) != Environment:
            raise Exception('Instance of Environment must be passed')

        self.environment_instance = environment

        self['environment'] = environment['_id']

        return self

    def get_environment(self):
        if self.environment_instance is not None:
            return self.environment_instance

        if type(self['environment']) is not ObjectId:
            raise Exception('Environment not specified')

        self.environment_instance = self.connection.Environment.find_one({'_id': self['environment']})

        if self.environment_instance is None:
            raise Exception('Environment not found')

        return self.environment_instance

    def set_version(self, version):
        self['version'] = version
        return self

    def set_file(self, file):
        if type(file) is not FileStorage:
            raise Exception('FileStorage instance must be passed')

        filename = unicode(secure_filename(file.filename))
        real_file_name = os.path.join(os.getcwd(), 'public', current_app.config['DISTRIBUTIVE_DIR'], filename)
        file.save(real_file_name)

        self['file'] = filename

        return self

    def get_url(self):
        return 'http://' + current_app.config['HOSTNAME'] + '/' + os.path.join(current_app.config['DISTRIBUTIVE_DIR'], self['file'])

    def is_file_attached(self):
        return bool(self['file'])