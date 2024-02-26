from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import Register, Login, AdminLogin
from models import db

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

# Configure your Flask app as before
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config["JWT_SECRET_KEY"] = "super-secret"
CORS(app)
db.init_app(app)
api = Api(app)
jwt = JWTManager(app)

# Add resources to API
api.add_resource(Register, '/register')
api.add_resource(Login, '/learners-login')
api.add_resource(AdminLogin, '/admin-login')

# REST API route
@app.route('/http-call')
def http_call():
    data = {'data': 'This is a response from the server'}
    return jsonify(data)

# WebSocket events
@socketio.on('connect')
def connected():
    print(request.sid)
    print('client is connected')
    emit("connected", {'data': f"id: {request.sid} is connected"})
    
@socketio.on('disconnect')
def disconnect():
    print('client is disconnected')
    emit("disconnect", f"user {request.sid} is disconnected", broadcast=True)
    
@socketio.on('data')
def handle_message(data):
    print('Data from the front end: ', str(data))
    emit('data', {'data': data, 'id': request.sid}, broadcast=True)

if __name__ == '__main__':
    # Run the application with both REST API and WebSocket support
    socketio.run(app, debug=True, port=5555)
