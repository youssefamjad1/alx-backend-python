#!/usr/bin/env python3
"""
Custom class-based context manager for Database connection
"""

import sqlite3


class DatabaseConnection:
    """
    A context manager class that handles database connections
    automatically using __enter__ and __exit__ methods
    """
    
    def __init__(self, db_name="example.db"):
        """
        Initialize the DatabaseConnection with database name
        
        Args:
            db_name (str): Name of the database file
        """
        self.db_name = db_name
        self.connection = None
        self.cursor = None
    
    def __enter__(self):
        """
        Called when entering the 'with' statement
        Opens the database connection and returns the cursor
        
        Returns:
            sqlite3.Cursor: Database cursor for executing queries
        """
        print(f"Opening database connection to {self.db_name}")
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            return self.cursor
        except sqlite3.Error as e:
            print(f"Error opening database: {e}")
            raise
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Called when exiting the 'with' statement
        Closes the database connection and handles any exceptions
        
        Args:
            exc_type: Exception type (if any)
            exc_val: Exception value (if any)
            exc_tb: Exception traceback (if any)
        
        Returns:
            bool: False to propagate exceptions, True to suppress them
        """
        if self.cursor:
            self.cursor.close()
            print("Database cursor closed")
        
        if self.connection:
            if exc_type is None:
                # No exception occurred, commit any pending transactions
                self.connection.commit()
                print("Database transaction committed")
            else:
                # Exception occurred, rollback any pending transactions
                self.connection.rollback()
                print(f"Database transaction rolled back due to: {exc_val}")
            
            self.connection.close()
            print("Database connection closed")
        
        # Return False to propagate any exceptions that occurred
        return False


def setup_database():
    """
    Setup a sample database with users table for testing
    """
    with sqlite3.connect("example.db") as conn:
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                age INTEGER
            )
        ''')
        
        # Insert sample data
        users_data = [
            (1, 'Alice Johnson', 'alice@example.com', 25),
            (2, 'Bob Smith', 'bob@example.com', 30),
            (3, 'Charlie Brown', 'charlie@example.com', 35),
            (4, 'Diana Wilson', 'diana@example.com', 28)
        ]
        
        cursor.execute('DELETE FROM users')  # Clear existing data
        cursor.executemany(
            'INSERT OR REPLACE INTO users (id, name, email, age) VALUES (?, ?, ?, ?)',
            users_data
        )
        
        conn.commit()
        print("Sample database setup completed")


def main():
    """
    Main function to demonstrate the DatabaseConnection context manager
    """
    # Setup the database with sample data
    setup_database()
    
    print("\n" + "="*50)
    print("Using DatabaseConnection context manager")
    print("="*50)
    
    # Use the context manager to query the database
    with DatabaseConnection("example.db") as cursor:
        try:
            # Execute the required query
            cursor.execute("SELECT * FROM users")
            results = cursor.fetchall()
            
            print("\nQuery Results from 'SELECT * FROM users':")
            print("-" * 40)
            print(f"{'ID':<5} {'Name':<15} {'Email':<25} {'Age':<5}")
            print("-" * 40)
            
            for row in results:
                print(f"{row[0]:<5} {row[1]:<15} {row[2]:<25} {row[3]:<5}")
            
            print(f"\nTotal users found: {len(results)}")
            
        except sqlite3.Error as e:
            print(f"Database error occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    print("\n" + "="*50)
    print("Context manager demonstration completed")
    print("="*50)


if __name__ == "__main__":
    main()