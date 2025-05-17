#!/usr/bin/python3
import mysql.connector
from decimal import Decimal

def stream_users():
    # Connect to your ALX_prodev database
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="20252025",
        database="ALX_prodev"
    )
    cursor = db.cursor(dictionary=True)  # return rows as dict

    cursor.execute("SELECT * FROM user_data")

    # One loop to yield each row one by one
    for row in cursor:
        # Convert Decimal age to int
        if isinstance(row['age'], Decimal):
            row['age'] = int(row['age'])
        yield row

    cursor.close()
    db.close()
