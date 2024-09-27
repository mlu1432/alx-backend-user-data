#!/usr/bin/env python3
"""
DB module to manage interactions with the database.
"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
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
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.
        
        :param email: The email of the user.
        :param hashed_password: The hashed password of the user.
        :return: The created User object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user by arbitrary keyword arguments.
        
        :param kwargs: Arbitrary keyword arguments for filtering.
        :return: The User object if found.
        :raises NoResultFound: If no user is found.
        :raises InvalidRequestError: If invalid query arguments are passed.
        """
        try:
            return self._session.query(User).filter_by(**kwargs).first()
        except NoResultFound:
            raise NoResultFound("No user found with the given parameters.")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid query parameters.")

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user's attributes.
        
        :param user_id: The ID of the user to update.
        :param kwargs: Arbitrary keyword arguments for updating the user.
        :raises ValueError: If an invalid attribute is passed.
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f"Invalid attribute: {key}")
            setattr(user, key, value)
        self._session.commit()
