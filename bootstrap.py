# Import Flask
from flask import Flask
from flask_login import LoginManager

# Import routes
from routes.api import api
from routes.site import site
from routes.auth import auth

# Import models
from models.user import User
from models.distributive import Distributive
from models.environment import Environment

# Import internal libs
import os

# Import external libs
from mongokit import Connection
from bson.objectid import ObjectId

# Create app
app = Flask(__name__)

# Configure app
app.config.from_object('configs.default.Config')

env = os.getenv('APPLICATION_ENV', 'development')
app.config.from_object('configs.' + env + '.Config')

# Register routes
app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)

# Database connection
app.connection = Connection(app.config['MONGODB_HOST'], app.config['MONGODB_PORT'])
app.connection.register([User])
app.connection.register([Distributive])
app.connection.register([Environment])

# Login manager
loginManager = LoginManager()
loginManager.login_view = 'auth.login'
loginManager.init_app(app)

@loginManager.user_loader
def load_user(email):
    user = app.connection.User.find_one({'email': email})
    return user

# Run app
if __name__ == "__main__":
    app.run(port=app.config['PORT'])

