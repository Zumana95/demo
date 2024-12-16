from flask import Blueprint

# Create a blueprint for the errors
errors = Blueprint('errors', __name__)

# Import the error handlers
from flaskblog.errors import handlers

