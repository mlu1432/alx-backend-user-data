## Personal Data Management System
- This project provides a secure and robust solution for handling personally identifiable information (PII). The system leverages Python to securely manage user data, including hashing passwords, validating them, and obfuscating sensitive information from logs. It includes functionalities for securely interacting with a MySQL database while ensuring that sensitive information such as passwords, phone numbers, and social security numbers are not exposed.

# Features

- Password Hashing: User passwords are securely hashed using the bcrypt library to ensure that no plain-text passwords are stored in the database.

Password Validation: Provides functionality to validate user passwords against stored hashed passwords.

Secure Logging: Sensitive PII data like name, email, phone, ssn, and password are obfuscated in logs to prevent exposure of private information.

- Database Interaction: The system securely connects to a MySQL database using environment variables for credentials, which ensures that credentials are not hardcoded into the codebase.

## Project Structure

- encrypt_password.py: Contains functions to hash passwords using bcrypt and validate passwords by comparing them with their hashed versions.
- filtered_logger.py: Provides functionality for logging with sensitive PII fields obfuscated, and handles database connections.
- main.py: A testing script that demonstrates the usage of password hashing and validation as well as logging filtered information.
- main.sql: SQL script for setting up the MySQL database and creating the necessary users table with sample data.
user_data.csv: Sample user data in CSV format.
