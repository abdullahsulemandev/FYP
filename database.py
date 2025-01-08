import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

DB_PATH = 'database.db'

# Initialize the database and create tables if they don't exist
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        # Create users table
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL
                     )''')

        # Create feedback table
        c.execute('''CREATE TABLE IF NOT EXISTS feedback (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        feedback_text TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                     )''')

        # Create filters table using user_email as a foreign key
        c.execute('''CREATE TABLE IF NOT EXISTS filters (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_email TEXT NOT NULL,
                        filter TEXT NOT NULL,
                        video_id TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_email) REFERENCES users (email)
                    )''')

        # Create happy_clients table
        c.execute('''CREATE TABLE IF NOT EXISTS happy_clients (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         name TEXT NOT NULL,
                         email TEXT NOT NULL
                    )''')
        # create video analyzed
        
        c.execute('''CREATE TABLE IF NOT EXISTS stats (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        happy_clients_count INTEGER DEFAULT 0,
                        videos_analyzed_count INTEGER DEFAULT 0
                    )''')

        # Ensure stats table has an initial row
        c.execute('INSERT OR IGNORE INTO stats (id, happy_clients_count, videos_analyzed_count) VALUES (1, 0, 0)')


        conn.commit()

# Add a new user with hashed password to the users table
def add_user(email, password):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            hashed_password = generate_password_hash(password)
            c.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, hashed_password))
            conn.commit()

            # Increment happy clients count
            increment_happy_clients_count()
            return True
    except sqlite3.IntegrityError:
        print("Error: User with this email already exists.")
        return False
    except Exception as e:
        print(f"Error adding user: {e}")
        return False

# Verify user credentials by checking the hashed password
def check_user_credentials(email, password):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('SELECT password FROM users WHERE email = ?', (email,))
            result = c.fetchone()
            return result and check_password_hash(result[0], password)
    except Exception as e:
        print(f"Error checking credentials: {e}")
        return False

# Find a user by their email address
def find_user_by_email(email):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('SELECT id, email FROM users WHERE email = ?', (email,))
            return c.fetchone()
    except Exception as e:
        print(f"Error finding user: {e}")
        return None

# Update user's password
def update_user_password(email, new_password):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            hashed_password = generate_password_hash(new_password)
            c.execute('UPDATE users SET password = ? WHERE email = ?', (hashed_password, email))
            conn.commit()
            return c.rowcount > 0
    except Exception as e:
        print(f"Error updating password: {e}")
        return False

# Save feedback to the database
def save_feedback(user_id, feedback_text):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('INSERT INTO feedback (user_id, feedback_text) VALUES (?, ?)', (user_id, feedback_text))
            conn.commit()
    except Exception as e:
        print(f"Error saving feedback: {e}")

# Get all feedback from the database
def get_all_feedback():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('''SELECT feedback.feedback_text, feedback.timestamp, users.email
                         FROM feedback
                         INNER JOIN users ON feedback.user_id = users.id
                         ORDER BY feedback.timestamp DESC''')
            return c.fetchall()
    except Exception as e:
        print(f"Error retrieving feedback: {e}")
        return []

# Save a detected filter to the database
def save_detected_filter(user_email, detected_filter, video_id):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            c.execute('INSERT INTO filters (user_email, filter, video_id, timestamp) VALUES (?, ?, ?, ?)',
                      (user_email, detected_filter, video_id, timestamp))
            conn.commit()
            return True
    except Exception as e:
        print(f"Error saving filter: {e}")
        return False

# Get the count of happy clients
def get_happy_clients_count():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('SELECT happy_clients_count FROM stats WHERE id = 1')
            result = c.fetchone()
            return result[0] if result else 0
    except Exception as e:
        print(f"Error fetching happy clients count: {e}")
        return 0

# Increment the happy clients count
def increment_happy_clients_count():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('UPDATE stats SET happy_clients_count = happy_clients_count + 1 WHERE id = 1')
            conn.commit()
    except Exception as e:
        print(f"Error incrementing happy clients count: {e}")
        
# Get the count of analyzed videos
def get_videos_analyzed_count():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('SELECT videos_analyzed_count FROM stats WHERE id = 1')
            result = c.fetchone()
            return result[0] if result else 0
    except Exception as e:
        print(f"Error fetching videos analyzed count: {e}")
        return 0

# Increment the videos analyzed count
def increment_videos_analyzed_count():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('UPDATE stats SET videos_analyzed_count = videos_analyzed_count + 1 WHERE id = 1')
            conn.commit()
    except Exception as e:
        print(f"Error incrementing videos analyzed count: {e}")

