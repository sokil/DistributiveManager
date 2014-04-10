# Import Flask
from flask import Flask, request
from flask_login import LoginManager
from flask_babel import Babel

# Import routes
from routes.api import api
from routes.environment import environment
from routes.distributive import distributive
from routes.auth import auth
from routes.user import user

# Import models
from models.user import User
from models.distributive import Distributive
from models.environment import Environment

# Import internal libs
import os

# Import external libs
from mongokit import Connection

# Create app
app = Flask(__name__)

# Configure app
app.config.from_object('configs.default.Config')

env = os.getenv('APPLICATION_ENV', 'development')
app.config.from_object('configs.' + env + '.Config')

# Register routes
app.register_blueprint(auth)
app.register_blueprint(environment)
app.register_blueprint(distributive)
app.register_blueprint(api)
app.register_blueprint(user)

# Database connection
app.connection = Connection(app.config['MONGODB_HOST'], app.config['MONGODB_PORT'])
app.connection.register([User])
app.connection.register([Distributive])
app.connection.register([Environment])

# Login manager
app.loginManager = LoginManager()
app.loginManager.login_view = 'auth.login'
app.loginManager.init_app(app)

@app.loginManager.user_loader
def load_user(email):
    return app.connection.User.find_one({'email': email})

# Localization
app.babel = Babel(app)

@app.babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['SUPPORTED_LANGUAGES'])

# Log errors
if app.config['LOGGER_ENABLED'] and len(app.config['LOGGER_EMAILS']) > 0:
    import logging
    from logging.handlers import SMTPHandler
    mail_handler = SMTPHandler(
        app.config['SMTP_HOST'],
        app.config['SMTP_FROM'],
        app.config['LOGGER_EMAILS'],
        'Distributive Manager error'
    )
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

# Run app
if __name__ == "__main__":
    app.run(port=app.config['PORT'])

