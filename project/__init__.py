import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

# Instantiate the app
app	= Flask(__name__)


# Set Configuration
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

# Instanciate Database
db = SQLAlchemy(app)

from project.api.views import user_blueprint
app.register_blueprint(user_blueprint)