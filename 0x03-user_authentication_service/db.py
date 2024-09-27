#!/usr/bin/env python3
"""
DB module to manage interactions with the database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.exc import NoResultFound
from user import Base, User


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
        """
        Add a new user to the database.

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
        Find a user by arbitrary keyword arguments in the database.

        Args:
            **kwargs: Arbitrary keyword arguments used to filter the user
            (e.g., email, id).

        Returns:
            User: The user object that matches the given filters.

        Raises:
            NoResultFound: If no user is found that matches the given filters
        """
        user = self._session.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user's attributes in the database.

        Args:
            user_id (int): The ID of the user to be updated.
            **kwargs: Arbitrary keyword arguments representing
            the attributes to be updated.

        Raises:
            ValueError: If any of the keys in kwargs do not correspond
            to valid user attributes.
        """
        user = self.find_user_by(id=user_id)

        # List of valid user attributes
        valid_attributes = ['email', 'hashed_password', 'session_id', 'reset_token']

        # Iterate over the keyword arguments to update user attributes
        for key, value in kwargs.items():
            if key not in valid_attributes:
                raise ValueError(f"{key} is not a valid attribute.")
            setattr(user, key, value)

        self._session.commit()
        return None
