#!/usr/bin/env python3
"""filtered_logger module."""


import re
from typing import List, Tuple, Union
import logging


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    """
    filter_datum: returns the log message obfuscated.

    Args:
        fields (List[str]): a list of strings representing all fields \
            to obfuscate.
        redaction (str): a string representing by what the field will \
            be obfuscated.
        message (str): a string representing the log line.
        separator (str): a string representing by which character is \
            separating all fields in the log line (message).

    Returns:
        str: the log message obfuscated.
    """
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class."""
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Constructor method."""
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """Filter values in incoming log records using filter_datum."""
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)
