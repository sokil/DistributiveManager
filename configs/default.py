class Config(object):
    HOSTNAME = 'dl'

    PORT = 9001
    DEBUG = True

    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017

    SECRET_KEY = 'fa+hq4;tr7q4@ra8*t62^783,.87'

    DISTRIBUTIVE_DIR = 'dist'

    PERMANENT_SESSION_LIFETIME = 1200

    LOGGER_ENABLED = True
    LOGGER_EMAILS = []

    SMTP_FROM = None
    SMTP_HOST = '127.0.0.1'