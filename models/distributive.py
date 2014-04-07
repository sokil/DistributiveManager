import re
import os
from mongokit import Document
from bson.objectid import ObjectId
from models.environment import Environment
from flask import current_app, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage


class Distributive(Document):
    __database__ = 'dl'
    __collection__ = 'distributives'

    environment_instance = None

    structure = {
        'version': {
            'number': int,
            'caption': unicode
        },
        'environment': ObjectId,
        'file': unicode
    }

    default_values = {
        'version.caption': '',
        'file': ''
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

        # test
        regex = re.compile(r'^([0-9]+)(?:\.([0-9]+)(?:\.([0-9]+)(?:-([0-9a-zA-Z\-\.]+))?)?)?$', re.IGNORECASE)
        match = regex.match(version)
        if match is None:
            raise Exception('Version format is wrong')

        # str
        self['version']['caption'] = version

        # str to int
        groups = match.groups()
        print groups;
        int_version = int(groups[0]) * 10000000
        if groups[1]:
            int_version += int(groups[1]) * 10000

        if groups[2]:
            int_version += int(groups[2]) * 10

        if groups[3] is None:
            int_version += 1;

        self['version']['number'] = int_version

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