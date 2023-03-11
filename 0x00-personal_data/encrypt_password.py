#!/usr/bin/env python3
"""encrypt_password module."""


import bcrypt


def hash_password(password: str) -> bytes:
    """hash_password: hashes a UNICODE string password using bcrypt.

    Args:
        password (str): a UNICODE string representing the password to hash.

    Returns:
        bytes: a salted, hashed password, which is a byte string.
    """
    return bcrypt.hashpw(password.encode('UTF8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """is_valid: validates that the provided password matches the hashed
    password.

    Args:
        hashed_password (bytes): a salted, hashed password, which is a byte
        string.
        password (str): a UNICODE string representing the password to hash.

    Returns:
        bool: True if the provided password matches the hashed password,
        otherwise False.
    """
    return bcrypt.checkpw(password.encode('UTF8'), hashed_password)
