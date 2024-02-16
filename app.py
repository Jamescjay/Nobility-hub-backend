from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import jwt
import random
import string

app = Flask(__name__)

SECRET_KEY = '905678'  

# Dummy admin data
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
    
    
if __name__ == '__main__':
    app.run(debug=True)
