#!/usr/bin/env python3
"""
This module contains a function to obfuscate specific fields in a log message
using regular expressions.
"""

import re
from typing import List

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
