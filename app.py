from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import jwt
import random
import string

app = Flask(__name__)

SECRET_KEY = '905678'  

# admin data for the test
admin_data = {'email': 'admin@moringaschool.com', 'password': 'password'}

# Dictionary to store user details
user_data = {'admin@moringaschool.com': admin_data}

@app.route('/')
def index():
    return '<h1>Welcome to the back end of the application</h1>'

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Check if JSON data is provided
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"success": False, "message": "Invalid request format"}), 400

    # Check login credentials
    if data['email'] in user_data and data['password'] == user_data[data['email']]['password']:
        expiration_time = datetime.utcnow() + timedelta(hours=1)
        token = jwt.encode({'email': data['email'], 'exp': expiration_time}, SECRET_KEY, algorithm='HS256')

        return jsonify({"success": True, "message": "Login successful", "token": token, 'user_email': data['email'], 'role': 'admin'}), 200
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401
    
@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    data = request.get_json()

    # Check if JSON data is provided
    if not data or 'email' not in data:
        return jsonify({"success": False, "message": "Invalid request format"}), 400

    user_email = data['email']

    # Check if the provided email exists
    if user_email in user_data:
        # Generate a new password
        new_password = generate_new_password()
        user_data[user_email]['password'] = new_password

        return jsonify({"success": True, "message": f"Password updated successfully. New password: {new_password}"}), 200
    else:
        return jsonify({"success": False, "message": "Invalid email"}), 401

def generate_new_password():
    # Generate a random password
    password_length = 10
    characters = string.ascii_letters + string.digits + string.punctuation
    new_password = ''.join(random.choice(characters) for i in range(password_length))
    return new_password
    
if __name__ == '__main__':
    app.run(debug=True)
