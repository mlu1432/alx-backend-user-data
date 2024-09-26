#!/usr/bin/env python3
"""
DB module to manage interactions with the database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.exc import NoResultFound, InvalidRequestError
from typing import TypeVar
from user import Base, User


DATA = ['id', 'email', 'hashed_password', 'session_id', 'reset_token']


class DB:
    """DB class to manage the database."""

    def __init__(self) -> None:
        """Initialize a new DB instance."""
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """Create and cache session object."""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database.

        Args:
            email (str): The email of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The newly created User object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Locate a user in the database by specific criteria.

        Args:
            **kwargs: Arbitrary keyword arguments representing
            the search filters.

        Returns:
            User: The user object that matches the given criteria.

        Raises:
            NoResultFound: If no user is found with the given filters.
            InvalidRequestError: If the query parameters are invalid.
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if not user:
                raise NoResultFound
            return user
        except AttributeError as e:
            # Catch invalid attribute filters
            raise InvalidRequestError from e
