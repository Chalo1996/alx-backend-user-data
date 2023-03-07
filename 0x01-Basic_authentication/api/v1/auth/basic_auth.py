#!/usr/bin/env python3
"""basic auth module."""


from api.v1.auth.auth import Auth
from models.user import User
import base64
from typing import TypeVar


class BasicAuth(Auth):
    """Basic authentication class."""
