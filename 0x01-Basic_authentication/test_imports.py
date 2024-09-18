"""test_imports.py"""
try:
    from flask import Flask, json
    from itsdangerous import json as itsdangerous_json  # This import should fail if itsdangerous v2.0.1 is installed
    print("Success: All modules imported correctly!")
except ImportError as e:
    print(f"ImportError: {e}")
