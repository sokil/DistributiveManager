from flask import Flask
import os
from routes.api import api

app = Flask(__name__)

# Register routes
app.register_blueprint(api)

# Configure app
app.config.from_object('configs.default.Config')

env = os.getenv('APPLICATION_ENV', 'development')
app.config.from_object('configs.' + env + '.Config')

# Run app
if __name__ == "__main__":
    app.run(port=app.config['PORT'])

