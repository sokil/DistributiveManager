# Import Flask
from flask import Flask
from flask_login import LoginManager

# Import routes
from routes.api import api
from routes.environment import environment
from routes.distributive import distributive
from routes.auth import auth
from routes.users import users

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
app.register_blueprint(users)

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

