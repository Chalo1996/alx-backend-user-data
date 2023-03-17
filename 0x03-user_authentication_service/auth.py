#!/usr/bin/env python3
"""Auth module"""

from db import DB, NoResultFound
from user import User
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash a password
    Args:
        password (str): The password
    Returns:
        str: The hashed password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        register_user: Register a user with a hashed password in the database


        Args:
            email (str): User email
            password (str): User password

        Returns:
            None
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            hashed_password = _hash_password(password)
            newUser = User(email=email, hashed_password=hashed_password)
            self._db.add_user(email=email, hashed_password=hashed_password)
        return newUser