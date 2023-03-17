#!/usr/bin/env python3
"""DB module
"""


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


from typing import Union, Dict, Any

from user import Base
from user import User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a user to the database
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by keyword arguments

        Args:
            kwargs (Dict[str, Any]): The keyword arguments

        Raises:
            NoResultFound: If the user is not found
            InvalidRequestError: If the keyword argument is not a \
                valid attribute

        Returns:
            Union[User, None]: The user or None
        """
        getUser = \
            self._session.query(User).filter_by(**kwargs).first()
        if getUser is None:
            raise NoResultFound
        if not getUser:
            raise InvalidRequestError
        return getUser

    def update_user(self, user_id: int, **kwargs: Dict[str, Any]) -> None:
        """Update a user by keyword arguments

        Args:
            user_id (int): The user id
            kwargs (Dict[str, Any]): The keyword arguments

        Raises:
            ValueError: If the keyword argument is not a valid attribute

        Returns:
            None: Nothing
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError
            setattr(user, key, value)
        self._session.commit()
