# Basic Authentication - Simple API
- This project is a simple API that implements basic authentication for user management. The API includes features for user creation, authentication, and authorization. Throughout the tasks, you will implement a basic authentication system from scratch.

# Table of Contents
- Requirements
- Project Structure
- Setup Instructions
- Running the API
- API Endpoints
## Authentication Overview

# Tasks
- Task 0: Simple-basic-API
- Task 1: Error handler - Unauthorized
- Task 2: Error handler - Forbidden
- Task 3: Auth class
- Task 4: Define which routes don’t need authentication
- Task 5: Request validation
- Task 6: Basic auth
- Task 7: Basic - Base64 part
- Task 8: Basic - Base64 decode
- Task 9: Basic - User credentials
- Task 10: Basic - User object
- Task 11: Basic - Overload current_user
- Task 12: Basic - Allow password with “:”
- Task 13: Require auth with stars

## Files

### `models/`

- `base.py`: base of all models of the API - handle serialization to file
- `user.py`: user model

### `api/v1`

- `app.py`: entry point of the API
- `views/index.py`: basic endpoints of the API: `/status` and `/stats`
- `views/users.py`: all users endpoints


## Setup

```
$ pip3 install -r requirements.txt
```


## Run

```
$ API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
```


## Routes

- `GET /api/v1/status`: returns the status of the API
- `GET /api/v1/stats`: returns some stats of the API
- `GET /api/v1/users`: returns the list of users
- `GET /api/v1/users/:id`: returns an user based on the ID
- `DELETE /api/v1/users/:id`: deletes an user based on the ID
- `POST /api/v1/users`: creates a new user (JSON parameters: `email`, `password`, `last_name` (optional) and `first_name` (optional))
- `PUT /api/v1/users/:id`: updates an user based on the ID (JSON parameters: `last_name` and `first_name`)
