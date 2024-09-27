 #!/usr/bin/env python3
"""
Basic Flask app
"""

from flask import Flask, jsonify

# Initialize Flask app
app = Flask(__name__)

# Define a route for GET requests to "/"
@app.route('/', methods=['GET'])
def welcome():
    """Route to return a welcome message in JSON format."""
    return jsonify({"message": "Bienvenue"})

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
