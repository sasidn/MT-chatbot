from flask import Blueprint

# Create the blueprint instances
chat_bp = Blueprint('chat', __name__)
main_bp = Blueprint('main', __name__)

# Import the route handlers
from .chat import chat_bp
from .main import main_bp

# Register the blueprints with the Flask application
def register_blueprints(app):
    app.register_blueprint(chat_bp)
    app.register_blueprint(main_bp)

# Optionally, you can define any additional setup or configuration for the routes module

# Import any other necessary modules or dependencies

# Call the register_blueprints function to register the blueprints
def init_app(app):
    register_blueprints(app)
    # Perform any other initialization or configuration tasks if needed

