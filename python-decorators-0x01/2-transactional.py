#!/usr/bin/env python3
import sqlite3
import functools

# ✅ Reusing your previous connection handler
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# ✅ New decorator: handles commit and rollback
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)  # Run the DB operation
            conn.commit()  # Commit if successful
            return result
        except Exception as e:
            conn.rollback()  # Rollback if there’s an error
            raise e
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# ✅ Test the function
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
