from flask import current_app, url_for
from flask_babel import gettext
from mongokit import Document, ValidationError


class Environment(Document):
    __database__ = 'dl'
    __collection__ = 'environment'

    structure = {
        'name': unicode
    }

    default_values = {
        'name': ''
    }

    def validate(self, auto_migrate=False, *args, **kwargs):
        # Validate unique name
        unique_check_query = {
            'name': self['name']
        }
        if '_id' in self and self['_id']:
            unique_check_query['_id'] = {'$ne': self['_id']}
        if current_app.connection.Environment.find_one(unique_check_query):
            raise ValidationError(gettext('Environment with same name already exists'))

        super(Environment, self).validate(*args, **kwargs)

    def get_latest_distributive(self):
        distributives = current_app.connection.Distributive.find({'environment': self['_id']}, sort=[('version.number', -1)], limit=1)

        try:
            distributive = distributives[0]
        except IndexError:
            distributive = None

        return distributive

    def get_latest_distributive_url(self):
        return 'http://' + current_app.config['SERVER_NAME'] + url_for('distributive.distributive_download', environment_name=self['name'])

    def delete(self):
        # delete distributives
        for distributive in current_app.connection.Distributive.find({'environment': self['_id']}):
            distributive.delete()

        # delete envitonment
        super(Environment, self).delete()
