#!/usr/bin/env python3
import sqlite3
import functools

# ✅ Decorator that opens and closes the DB connection automatically
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')  # Open DB connection
        try:
            return func(conn, *args, **kwargs)  # Pass the connection to the function
        finally:
            conn.close()  # Ensure the connection is closed no matter what
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# ✅ Example call
user = get_user_by_id(user_id=1)
print(user)
