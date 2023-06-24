from flask import Blueprint, request, render_template
from message_processing import process_message  # Import from message_processing

chat_bp = Blueprint('chat', __name__)

@chat_bp.route("/chat")
def chat():
    username = request.args.get('username')
    return render_template('chat.html', username=username)

@chat_bp.route("/get_response")
def get_response():
    msg = request.args.get('msg')
    # Process the user's message using the AI model
    response = process_message(msg)
    return response
