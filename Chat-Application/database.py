import sqlite3
import hashlib
from datetime import datetime


DATABASE_NAME = "chat.db"


def get_connection():
    return sqlite3.connect(
        DATABASE_NAME,
        check_same_thread=False
    )


def initialize_database():

    conn = get_connection()
    cursor = conn.cursor()

    # Users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Rooms
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    # Messages
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room TEXT NOT NULL,
            username TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    # Default room
    cursor.execute("""
        INSERT OR IGNORE INTO rooms (name)
        VALUES (?)
    """, ("General",))

    conn.commit()
    conn.close()


def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()


def register_user(username, password):

    try:

        conn = get_connection()
        cursor = conn.cursor()

        hashed_password = hash_password(
            password
        )

        cursor.execute("""
            INSERT INTO users
            (username, password)
            VALUES (?, ?)
        """, (
            username,
            hashed_password
        ))

        conn.commit()
        conn.close()

        return True, "Registration successful."

    except sqlite3.IntegrityError:

        return False, "Username already exists."

    except Exception as e:

        return False, str(e)


def authenticate_user(username, password):

    conn = get_connection()
    cursor = conn.cursor()

    hashed_password = hash_password(
        password
    )

    cursor.execute("""
        SELECT id
        FROM users
        WHERE username = ?
        AND password = ?
    """, (
        username,
        hashed_password
    ))

    result = cursor.fetchone()

    conn.close()

    return result is not None


def create_room(room_name):

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO rooms (name)
            VALUES (?)
        """, (room_name,))

        conn.commit()
        conn.close()

        return True

    except sqlite3.IntegrityError:

        return False


def get_rooms():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM rooms
        ORDER BY name
    """)

    rooms = [
        row[0]
        for row in cursor.fetchall()
    ]

    conn.close()

    return rooms


def save_message(
    room,
    username,
    message
):

    timestamp = datetime.now().strftime(
        "%H:%M"
    )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO messages
        (room, username, message, timestamp)
        VALUES (?, ?, ?, ?)
    """, (
        room,
        username,
        message,
        timestamp
    ))

    conn.commit()
    conn.close()

    return timestamp


def get_message_history(room):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT username, message, timestamp
        FROM messages
        WHERE room = ?
        ORDER BY id ASC
    """, (room,))

    messages = cursor.fetchall()

    conn.close()

    return messages