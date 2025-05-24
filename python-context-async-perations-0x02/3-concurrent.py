#!/usr/bin/env python3
"""
Concurrent Asynchronous Database Queries using aiosqlite
"""

import asyncio
import aiosqlite


DB_NAME = "example.db"  # the DB used in Task 1


async def async_fetch_users():
    """
    Fetch all users asynchronously
    """
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            print("\nAll Users:")
            for user in users:
                print(user)
            return users


async def async_fetch_older_users():
    """
    Fetch users older than 40 asynchronously
    """
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            older_users = await cursor.fetchall()
            print("\nUsers older than 40:")
            for user in older_users:
                print(user)
            return older_users


async def fetch_concurrently():
    """
    Run both fetch operations concurrently
    """
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
