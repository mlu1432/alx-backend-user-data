#!/usr/bin/env python3
"""
DB class for managing users and interactions with the database.
"""

from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from typing import TypeVar
from user import Base, User


DATA = ['id', 'email', 'hashed_password', 'session_id', 'reset_token']


class DB:

    def __init__(self) -> None:
        """Initialize the database engine and session."""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """Memoize the session object."""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a user to the database.

        Args:
            email (str): User's email.
            hashed_password (str): User's hashed password.

        Returns:
            User: The user object created in the database.
        """
        if not email or not hashed_password:
            raise ValueError("Email and hashed password must be provided.")
        user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by arbitrary keyword arguments.

        Args:
            kwargs: Arbitrary arguments to filter users.

        Returns:
            User: The user found based on the filter criteria.

        Raises:
            NoResultFound: If no user is found.
        """
        user = self._session.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound("No user found with the given parameters.")
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update user attributes in the database.

        Args:
            user_id (int): The ID of the user to be updated.
            kwargs: Arbitrary user attributes to update.

        Raises:
            ValueError: If an attribute is invalid.
        """
        user = self.find_user_by(id=user_id)
        for key, val in kwargs.items():
            if key not in DATA:
                raise ValueError(f"Invalid attribute: {key}")
            setattr(user, key, val)
        self._session.commit()
        return None
