#!/usr/bin/env python3
"""
This module contains functions and classes for obfuscating PII in logs
and managing logger setup with redacted formatting.
"""

import logging
import re
from typing import List, Tuple

# PII fields that should be redacted in logs
PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Obfuscates field values in a log message.

    Args:
        fields (List[str]): List of field names to obfuscate.
        redaction (str): String to replace field values with.
        message (str): The log message to process.
        separator (str): Separator between fields in the log message.

    Returns:
        str: The obfuscated log message.
    """
    pattern = r'({}=)([^{}]+)'.format('|'.join(fields), separator)
    return re.sub(pattern, r'\1{}'.format(redaction), message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class to obfuscate sensitive
    information in log messages.
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize the formatter with the fields to redact."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record, redacting specified fields."""
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """
    Creates a logger that logs up to INFO level with a redacting formatter.

    Returns:
        logging.Logger: A logger with a RedactingFormatter and StreamHandler.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.addHandler(stream_handler)

    return logger
