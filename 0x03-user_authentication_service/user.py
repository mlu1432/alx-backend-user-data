#!/usr/bin/env python3
"""User model definition for the 'users' table """

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


# Base class to inherit from
Base = declarative_base()


class User(Base):
    """
    User class that defines the 'users' table
    fields:
    - id : Integer primary key
    - email: Non-nullable string
    - hashed_password: Non-nullable string
    - session_id: Nullable string
    - reset_token: Nullable string
    """
    __tablename__ = 'users'


    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    def __init__(self, email: str, hashed_password: str):
        """Initialaze a new user instance"""
        self.email = email
        self.hashed_password = hashed_password
