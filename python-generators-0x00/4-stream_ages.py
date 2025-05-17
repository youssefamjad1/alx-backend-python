#!/usr/bin/python3
seed = __import__('seed')

def stream_user_ages():
    """Generator that yields user ages one by one"""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    rows = cursor.fetchall()
    connection.close()

    for row in rows:
        yield int(row['age'])
    return

def average_age():
    """Calculate average age using generator"""
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1
    if count == 0:
        print("No users found.")
        return
    print("Average age of users:", total / count)
