#!/usr/bin/env python3
"""filtered_logger module."""


import re
from typing import List
import logging
import os
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


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


def get_logger() -> logging.Logger:
    """get_logger: returns a logging.Logger object."""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to the database."""
    passwd = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db = os.getenv('PERSONAL_DATA_DB_NAME')

    conn = mysql.connector.connect(
        user=user, passwd=passwd, host=host, db=db)

    return conn


def main() -> None:
    """Obtain a database connection using get_db and retrieve all rows in the\
        users table and display each row under a filtered format.

    Returns:
        None: None.
    """

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = [i[0] for i in cursor.description]
    print('<<FIELD>>'.join([f'{field};' for field in fields]))
    logger = get_logger()

    for row in cursor:
        message = ''
        for i in range(len(fields)):
            message += f'{fields[i]}={row[i]};'
        print('ROW>>>>: '+str(row[i]))
        logger.info(message)

    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
