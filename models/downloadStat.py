from mongokit import Document
from bson.objectid import ObjectId
from datetime import datetime


class DownloadStat(Document):
    __database__ = 'dl'
    __collection__ = 'stat.download'

    structure = {
        'count': int,
        'time': datetime,
        'distributive_id': ObjectId
    }

    default_values = {
        'count': 0
    }

    @staticmethod
    def hit(distributive):
    # get time
        from datetime import datetime
        t = datetime.utcnow()
        t = t.replace(minute=t.minute - t.minute % 5, second=0, microsecond=0)

        # increment counter
        from flask import current_app
        return current_app.connection.DownloadStat.collection.update({
            'distributive_id': distributive['_id'],
            'time': t
        }, {
            '$inc': {'count': 1},
            '$set': {'environment_id': distributive['environment']}
        }, upsert=True)