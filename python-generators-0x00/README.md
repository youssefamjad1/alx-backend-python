# Python Generators - 0x00

## Task 0: Getting Started with Python Generators

### Objective
Create a Python script that sets up a MySQL database, populates it with data, and prepares it for use with Python generators to stream rows one by one.

### Description

This task demonstrates:

- Connecting to a MySQL server.
- Creating a new database `ALX_prodev`.
- Creating a table `user_data` with fields:
  - `user_id` (Primary Key, UUID, Indexed)
  - `name` (VARCHAR, NOT NULL)
  - `email` (VARCHAR, NOT NULL)
  - `age` (DECIMAL, NOT NULL)
- Importing user data from a CSV file (`user_data.csv`).
- Ensuring no duplicate email entries are inserted.

### Table Schema

```sql
CREATE TABLE user_data (
    user_id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    age DECIMAL NOT NULL,
    INDEX(user_id)
);
