#!/usr/bin/python3
import mysql.connector
from decimal import Decimal

def stream_users_in_batches(batch_size):
    """Generator that yields batches of users from the database"""
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='20252025',
        database='ALX_prodev'
    )
    cursor = connection.cursor(dictionary=True)
    offset = 0

    while True:
        cursor.execute(
            "SELECT * FROM user_data LIMIT %s OFFSET %s",
            (batch_size, offset)
        )
        rows = cursor.fetchall()
        if not rows:
            break
        for row in rows:
            if isinstance(row['age'], Decimal):
                row['age'] = int(row['age'])
        yield rows
        offset += batch_size

    cursor.close()
    connection.close()

def batch_processing(batch_size):
    """Processes batches and yields users older than 25"""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                yield user
