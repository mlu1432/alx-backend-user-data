#!/usr/bin/env python3
"""
Module for logging, filtering PII data, and connecting to a secure database.
"""

import logging
import re
import os
import mysql.connector
from mysql.connector.connection import MySQLConnection
from typing import List, Tuple
from logging import Logger, StreamHandler

# Define the tuple of PII fields that should be redacted
PII_FIELDS: Tuple[str, ...] = ("name", "email", "ssn", "phone", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obfuscates the values of specified fields in a log message.

    Args:
        fields (List[str]): The list of field names to obfuscate.
        redaction (str): The string to replace the field value with.
        message (str): The log message to filter.
        separator (str): The separator between fields in the log message.

    Returns:
        str: The log message with obfuscated values.
    """
    for field in fields:
        message = re.sub(f'{field}=[^{separator}]*',
                         f'{field}={redaction}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class for obfuscating PII fields."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the RedactingFormatter.

        Args:
            fields (List[str]): List of fields to redact in the log message.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record and redact sensitive information.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log message with sensitive data redacted.
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super().format(record)


def get_logger() -> Logger:
    """
    Creates and configures a logger to handle sensitive information with
    a RedactingFormatter for PII fields.

    Returns:
        logging.Logger: The configured logger object.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    handler = StreamHandler()
    handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(handler)
    logger.propagate = False
    return logger


def get_db() -> MySQLConnection:
    """
    Returns a MySQL connection object using credentials stored in
    environment variables or via UNIX socket.

    If PERSONAL_DATA_DB_HOST is set to 'localhost', we connect via
    UNIX socket.
    """
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    # Use UNIX socket if connecting to localhost
    if host == "localhost":
        return mysql.connector.connect(
            user=username,
            password=password,
            unix_socket='/var/run/mysqld/mysqld.sock',
            database=db_name
        )
    else:
        return mysql.connector.connect(
            user=username,
            password=password,
            host=host,
            database=db_name
        )
