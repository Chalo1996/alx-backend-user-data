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
