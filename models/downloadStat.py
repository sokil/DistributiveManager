from mongokit import Document
from bson.objectid import ObjectId
from datetime import datetime
from flask import current_app


class DownloadStat(Document):
    __database__ = 'dl'
    __collection__ = 'stat.download'

    structure = {
        'count': int,
        'time': datetime
    }

    default_values = {
        'count': 0
    }

    @staticmethod
    def hit():
        # get time
        t = datetime.today()
        t = t.replace(minute=t.minute - t.minute % 5, second=0, microsecond=0)

        # increment counter
        print current_app.connection.DownloadStat.collection.update({'time': t}, {'$inc': {'count': 1}}, upsert=True)