#!/usr/bin/env python3
"""basic auth module."""


from api.v1.auth.auth import Auth
from models.user import User
import base64
from typing import TypeVar


class BasicAuth(Auth):
    """Basic authentication class."""

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """Returns the Base64 part of the Authorization header for a Basic Authentication."""
        if authorization_header is None or type(authorization_header) is not str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]
