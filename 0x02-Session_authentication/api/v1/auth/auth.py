#!/usr/bin/env python3
"""auth module."""

from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """authentication template."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require authentication."""
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path += '/'

        if path in excluded_paths:
            return False

        for excluded_path in excluded_paths:
            if excluded_path[-1] != '*':
                continue
            if path.startswith(excluded_path[:-1]):
                return False
        return True

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user."""
        return None

    def authorization_header(self, request=None) -> str:
        """Authorization header."""
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def session_cookie(self, request=None):
        """Session cookie."""
        if request is None:
            return None
        session_name = getenv('SESSION_NAME')
        return request.cookies.get(session_name)
