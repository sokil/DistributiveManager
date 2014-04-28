from flask import current_app, url_for

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

    def get_latest_distributive(self):
        distributives = current_app.connection.Distributive.find({'environment': self['_id']}, sort=[('version.number', -1)], limit=1)

        try:
            distributive = distributives[0]
        except IndexError:
            distributive = None

        return distributive


    def get_latest_distributive_url(self):
        return 'http://' + current_app.config['HOSTNAME'] + url_for('distributive.distributive_latest', environment_name=self['name'])

    def delete(self):
        # delete distributives
        for distributive in current_app.connection.Distributive.find({'environment': self['_id']}):
            distributive.delete()

        # delete envitonment
        super(Environment, self).delete();
