from flask import Blueprint, render_template, request, redirect, flash
from flask.globals import g
from message_processing import process_message


main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def home():
    chat_summarization_message = request.args.get('chat_summarization_message')
    mood_tracker_message = request.args.get('mood_tracker_message')
    username = request.args.get('username')

    return render_template('home.html', chat_summarization_message=chat_summarization_message, mood_tracker_message=mood_tracker_message, username=username)

@main_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Retrieve the database connection from the global context (assuming it's stored there)
        db = g.get('db')

        # Create a cursor object to interact with the database
        cursor = db.cursor()

        # Execute a SELECT query to check if the user exists
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        values = (username, password)
        cursor.execute(query, values)

        # Fetch the result
        result = cursor.fetchone()

        # Close the cursor
        cursor.close()

        if result:
            # User exists
            return render_template('home.html', message="Login successful", username=username)
        else:
            # User does not exist or incorrect password
            flash("Invalid credentials. Please try again!", "error")

    return render_template('login.html')

@main_bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']

        # Retrieve the database connection from the global context (assuming it's stored there)
        db = g.get('db')

        # Create a cursor object to interact with the database
        cursor = db.cursor()

        # Check if the username already exists in the database
        query = "SELECT * FROM users WHERE username = %s"
        values = (username,)
        cursor.execute(query, values)

        # Fetch the result
        result = cursor.fetchone()

        if result:
            # Username already exists
            cursor.close()
            flash("Username already exists. Please choose a different username.", "error")
        else:
            # Execute an INSERT query to add the user to the database
            query = "INSERT INTO users (username, name, password, email) VALUES (%s, %s, %s, %s)"
            values = (username, name, password, email)
            cursor.execute(query, values)

            # Commit the changes to the database
            db.commit()

            flash("User registered successfully", "success")

            return redirect("/")

        # Close the cursor
        cursor.close()

    return render_template('register.html')

@main_bp.route("/chat_summarization", methods=['GET', 'POST'])
def chat_summarization():
    if request.method == 'POST':
        username = request.form['username']

        # Retrieve the database connection from the global context (assuming it's stored there)
        db = g.get('db')

        # Create a cursor object to interact with the database
        cursor = db.cursor()

        # Execute a SELECT query to retrieve messages and user information
        query = "SELECT m.message_id,u.username,m.message,m.date FROM messages m JOIN users u ON m.user_id = u.user_id WHERE u.username = %s"
        values = (username,)
        cursor.execute(query, values)

        # Fetch the results
        messages = cursor.fetchall()

        # Close the cursor
        cursor.close()

        return render_template('chat_summarization.html', messages=messages)

    # For GET requests, redirect to the home page with a message
    username = request.args.get('username')
    return redirect(f"/?chat_summarization_message=Chat%20Summarization%20button%20clicked&username={username}", code=307)


@main_bp.route("/mood_tracker", methods=['GET', 'POST'])
def mood_tracker():
    if request.method == 'POST':
        username = request.form['username']

        # Retrieve the database connection from the global context (assuming it's stored there)
        db = g.get('db')

        # Create a cursor object to interact with the database
        cursor = db.cursor()

        # Execute a select query to get the mood information
        query = "SELECT m.sentiment, m.tracking_date FROM mood_tracker m JOIN users u ON m.user_id = u.user_id WHERE u.username = %s"
        values = (username,)
        cursor.execute(query, values)

        # Fetch the results
        messages = cursor.fetchall()

        # Close the cursor
        cursor.close()

        return render_template('mood_tracker.html', messages=messages)

    # For GET requests, redirect to the home page with a message
    username = request.args.get('username')
    return redirect(f"/?mood_tracker_message=Mood%20Tracker%20button%20clicked&username={username}", code=307)

@main_bp.route("/recommendations_log", methods=['GET', 'POST'])
def recommendations_log():
    if request.method == 'POST':
        username = request.form['username']

        # Retrieve the database connection from the global context (assuming it's stored there)
        db = g.get('db')

        # Create a cursor object to interact with the database
        cursor = db.cursor()

        # Execute a SELECT query to retrieve recommendations and associated messages for the user
        query = "SELECT r.recommendation, m.message FROM recommendations_log r JOIN messages m ON r.message_id = m.message_id JOIN users u ON m.user_id = u.user_id WHERE u.username = %s"
        values = (username,)
        cursor.execute(query, values)

        # Fetch the results
        messages = cursor.fetchall()

        # Close the cursor
        cursor.close()

        return render_template('recommendations_log.html', messages=messages)

    # For GET requests, redirect to the home page with a message
    username = request.args.get('username')
    return redirect(f"/?recommendations_log_message=Recommendations%20Log%20button%20clicked&username={username}", code=307)

@main_bp.route("/thought_diary", methods=['GET', 'POST'])
def thought_diary():
    if request.method == 'POST':
        username = request.form['username']

        # Retrieve the database connection from the global context (assuming it's stored there)
        db = g.get('db')

        # Create a cursor object to interact with the database
        cursor = db.cursor()

        # Execute a SELECT query to retrieve thought diary entries for the user
        query = "SELECT t.entry_date, t.situation, t.automatic_thought, t.mood_emotion, t.evidence, t.alternative_thought, t.outcome FROM thought_diary t JOIN users u ON u.user_id = t.user_id WHERE u.username = %s"
        values = (username,)
        cursor.execute(query, values)

        # Fetch the results
        thoughts = cursor.fetchall()

        # Close the cursor
        cursor.close()

        # After fetching the entries, redirect back to the thought diary page
        return render_template('thought_diary.html', thoughts=thoughts)

    # For GET requests, redirect to the home page with a message
    username = request.args.get('username')
    return redirect(f"/?thought_diary_message=Thought%20Diary%20button%20clicked&username={username}", code=307)
