import re
import os
from mongokit import Document
from bson.objectid import ObjectId
from models.environment import Environment
from flask import current_app, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage


class Distributive(Document):
    __database__ = 'dl'
    __collection__ = 'distributives'

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
        'file': u''
    }

    environment_instance = None

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

        # check if version already specified
        check_dist_existance_data = {
            'environment': self['environment'],
            'version.caption': version
        }

        if '_id' in self:
            check_dist_existance_data['_id'] = {'$ne', self['_id']}

        if current_app.connection.Distributive.find_one(check_dist_existance_data) is not None:
            raise Exception('Distributive with defined version already exists')

        # test
        regex = re.compile(r'^([0-9]+)(?:\.([0-9]+)(?:\.([0-9]+)(?:-([0-9a-zA-Z\-\.]+))?)?)?$', re.IGNORECASE)
        match = regex.match(version)
        if match is None:
            raise Exception('Version format is wrong')

        # str
        self['version']['caption'] = version

        # str to int
        groups = match.groups()

        int_version = int(groups[0]) * 10000000
        if groups[1]:
            int_version += int(groups[1]) * 10000

        if groups[2]:
            int_version += int(groups[2]) * 10

        if groups[3] is None:
            int_version += 1;

        self['version']['number'] = int_version

        return self

    def set_file(self, file, overwrite=False):

        if type(file) is not FileStorage:
            raise Exception('FileStorage instance must be passed')

        filename = unicode(secure_filename(file.filename))

        # check if file already exists
        if not overwrite:
            real_filename = os.path.join(self.get_storage_dir(), filename)
            if os.path.isfile(real_filename) and real_filename != self.get_path():
                raise Exception('File with same name already exists')

        # delete file if previously uploaded
        if self.is_file_attached():
            os.remove(self.get_path())

        # define new file name
        self['file'] = filename

        # save file
        file.save(self.get_path())

        return self

    def get_storage_dir(self):
        return os.path.join(os.getcwd(), 'public', current_app.config['DISTRIBUTIVE_DIR'])

    def get_path(self):
        return os.path.join(self.get_storage_dir(), self['file'])

    def get_url(self, canonical=True):
        url = '/' + os.path.join(current_app.config['DISTRIBUTIVE_DIR'], self['file'])

        if canonical:
            url = 'http://' + current_app.config['HOSTNAME'] + url

        return url

    def is_file_attached(self):
        return bool(self['file'])

    def delete(self):
        # delete file
        if self.is_file_attached() and os.path.isfile(self.get_path()):
            os.remove(self.get_path())

        # delete document
        super(Distributive, self).delete()