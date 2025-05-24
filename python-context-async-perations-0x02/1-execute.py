#!/usr/bin/env python3
"""
Reusable Query Context Manager
"""

import sqlite3


class ExecuteQuery:
    """
    A reusable context manager class that executes SQL queries
    and manages database connections automatically
    """
    
    def __init__(self, db_name, query, params=None):
        """
        Initialize the ExecuteQuery context manager
        
        Args:
            db_name (str): Name of the database file
            query (str): SQL query to execute
            params (tuple/list): Parameters for the query (optional)
        """
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.connection = None
        self.cursor = None
        self.results = None
    
    def __enter__(self):
        """
        Called when entering the 'with' statement
        Opens database connection, executes query, and returns results
        
        Returns:
            list: Query results
        """
        print(f"Opening database connection to {self.db_name}")
        try:
            # Open database connection
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            
            print(f"Executing query: {self.query}")
            if self.params:
                print(f"With parameters: {self.params}")
                # Execute query with parameters
                self.cursor.execute(self.query, self.params)
            else:
                # Execute query without parameters
                self.cursor.execute(self.query)
            
            # Fetch all results
            self.results = self.cursor.fetchall()
            print(f"Query executed successfully. {len(self.results)} rows returned.")
            
            return self.results
            
        except sqlite3.Error as e:
            print(f"Database error occurred: {e}")
            raise
        except Exception as e:
            print(f"An error occurred: {e}")
            raise
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Called when exiting the 'with' statement
        Closes database connection and handles any exceptions
        
        Args:
            exc_type: Exception type (if any)
            exc_val: Exception value (if any)
            exc_tb: Exception traceback (if any)
        
        Returns:
            bool: False to propagate exceptions
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
    print("Setting up sample database...")
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
        
        # Insert sample data with various ages
        users_data = [
            (1, 'Alice Johnson', 'alice@example.com', 25),
            (2, 'Bob Smith', 'bob@example.com', 30),
            (3, 'Charlie Brown', 'charlie@example.com', 35),
            (4, 'Diana Wilson', 'diana@example.com', 28),
            (5, 'Eve Davis', 'eve@example.com', 22),
            (6, 'Frank Miller', 'frank@example.com', 40),
            (7, 'Grace Lee', 'grace@example.com', 27),
            (8, 'Henry Taylor', 'henry@example.com', 32)
        ]
        
        cursor.execute('DELETE FROM users')  # Clear existing data
        cursor.executemany(
            'INSERT OR REPLACE INTO users (id, name, email, age) VALUES (?, ?, ?, ?)',
            users_data
        )
        
        conn.commit()
        print("Sample database setup completed with 8 users")


def display_results(results, title="Query Results"):
    """
    Display query results in a formatted table
    
    Args:
        results (list): Query results
        title (str): Title for the results table
    """
    print(f"\n{title}:")
    print("-" * 50)
    if results:
        print(f"{'ID':<5} {'Name':<15} {'Email':<25} {'Age':<5}")
        print("-" * 50)
        for row in results:
            print(f"{row[0]:<5} {row[1]:<15} {row[2]:<25} {row[3]:<5}")
        print(f"\nTotal records found: {len(results)}")
    else:
        print("No records found.")
    print("-" * 50)


def main():
    """
    Main function to demonstrate the ExecuteQuery context manager
    """
    # Setup the database with sample data
    setup_database()
    
    print("\n" + "="*60)
    print("Demonstrating ExecuteQuery Context Manager")
    print("="*60)
    
    # Example 1: Required query - users with age > 25
    print("\n1. Required Query: SELECT * FROM users WHERE age > ?")
    with ExecuteQuery("example.db", "SELECT * FROM users WHERE age > ?", (25,)) as results:
        display_results(results, "Users with age > 25")
    
    print("\n" + "="*60)
    
    # Example 2: Different query - users with age <= 30
    print("\n2. Additional Query: SELECT * FROM users WHERE age <= ?")
    with ExecuteQuery("example.db", "SELECT * FROM users WHERE age <= ?", (30,)) as results:
        display_results(results, "Users with age <= 30")
    
    print("\n" + "="*60)
    
    # Example 3: Query without parameters - all users
    print("\n3. Query without parameters: SELECT * FROM users")
    with ExecuteQuery("example.db", "SELECT * FROM users") as results:
        display_results(results, "All Users")
    
    print("\n" + "="*60)
    
    # Example 4: Query with specific name pattern
    print("\n4. Query with LIKE: SELECT * FROM users WHERE name LIKE ?")
    with ExecuteQuery("example.db", "SELECT * FROM users WHERE name LIKE ?", ('%son%',)) as results:
        display_results(results, "Users with 'son' in their name")
    
    print("\n" + "="*60)
    print("ExecuteQuery context manager demonstration completed")
    print("="*60)


if __name__ == "__main__":
    main()