# 0x02. Session Authentication
- This project focuses on implementing session-based authentication in a web API. It builds upon the previous Basic Authentication implementation and introduces the use of Session IDs stored in cookies to handle user authentication.


Tasks
- 0. Et moi et moi et moi!
# In this task, the objective is to set up a Session Authentication system.

Steps:
Copy all work from the 0x06. Basic authentication project.
Implement a new endpoint: GET /users/me to retrieve the authenticated user.
Update @app.before_request in api/v1/app.py to assign the result of auth.current_user(request) to request.current_user.
Update the route GET /api/v1/users/<user_id> to return the authenticated user when <user_id> is set to me.
- 1. Empty session
# Create a class SessionAuth that inherits from Auth.

Requirements:
The class should be created in api/v1/auth/session_auth.py.
Ensure it inherits correctly without any overloading.
Set up the environment variable AUTH_TYPE=session_auth to switch between Basic and Session Authentication in api/v1/app.py.
- 2. Create a session
# Update the SessionAuth class:

Requirements:
Add a class attribute user_id_by_session_id (dictionary) to store user IDs by session IDs.
Implement the method create_session(self, user_id: str = None) -> str to generate a session ID using uuid4() for the given user ID.
Store the session ID as the key and the user ID as the value in user_id_by_session_id.
- 3. User ID for Session ID
# Implement a method to retrieve the user ID based on the session ID:

Requirements:
Add the method user_id_for_session_id(self, session_id: str = None) -> str to retrieve the user ID from user_id_by_session_id dictionary using .get().
Return None if the session_id is None or not a string.
- 4. Session cookie
# Handle session IDs through cookies.

Requirements:
Add the method session_cookie(self, request=None) in api/v1/auth/auth.py.
Use the environment variable SESSION_NAME to define the cookie name for the session ID.
Return the value of the cookie from the request or None if the cookie doesn’t exist.
- 5. Before request
# Update the @app.before_request method to:

Requirements:
Add the path /api/v1/auth_session/login/ to the excluded paths list in auth.require_auth().
If neither auth.authorization_header(request) nor auth.session_cookie(request) return a value, abort with a 401 status code.
- 6. Use Session ID for identifying a User
# Link session IDs to user instances.

Requirements:
Implement current_user(self, request=None) in SessionAuth to return a User instance based on the session cookie.
Use session_cookie() and user_id_for_session_id() to retrieve the user ID from the session ID.
Use User.get(user_id) to retrieve the User instance.
- 7. New view for Session Authentication
# Create a new view for session authentication:

Requirements:
Create a new file api/v1/views/session_auth.py.
Implement the route POST /auth_session/login to:
Retrieve email and password from request.form.get().
Return appropriate error responses if email or password is missing.
Authenticate the user by checking the email and password.
If successful, create a session ID using auth.create_session(user_id) and return the user’s information as JSON.
Set the session ID in a cookie in the response.
- 8. Logout
# Implement session logout:

Requirements:
Add a method destroy_session(self, request=None) in SessionAuth to delete the user session.
Add a new route DELETE /api/v1/auth_session/logout to log the user out by removing their session ID from user_id_by_session_id.
If the session ID is invalid or missing, abort with a 404 error.
