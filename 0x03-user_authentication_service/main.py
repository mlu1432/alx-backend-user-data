#!/usr/bin/env python3
"""
Main file to test DB and User model functionalities
"""

from db import DB
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

my_db = DB()

# Test add_user
user_1 = my_db.add_user("test@test.com", "SuperHashedPwd")
print(f"User 1 ID: {user_1.id}")

user_2 = my_db.add_user("test1@test.com", "SuperHashedPwd1")
print(f"User 2 ID: {user_2.id}")

# Test find_user_by
try:
    find_user = my_db.find_user_by(email="test@test.com")
    print(f"Found User ID: {find_user.id}")
except NoResultFound:
    print("User not found.")

# Test find_user_by with invalid query
try:
    find_user = my_db.find_user_by(no_email="test@test.com")
except InvalidRequestError:
    print("Invalid query.")

# Test update_user
try:
    my_db.update_user(user_1.id, hashed_password="NewSuperHashedPwd")
    print("Password updated for User 1.")
except ValueError:
    print("Error updating user.")

