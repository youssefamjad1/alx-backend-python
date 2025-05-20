#!/usr/bin/env python3
import sqlite3
import functools

# Global dictionary to cache queries
query_cache = {}

# ✅ with_db_connection decorator from previous tasks
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# ✅ cache_query decorator
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print("Using cached result.")
            return query_cache[query]
        print("Query not cached. Executing and caching result.")
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# ✅ First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# ✅ Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
