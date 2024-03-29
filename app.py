from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS
from flask_mail import Mail, Message
from resources.user import Register, Login, AdminLogin
from resources.message import MessageResource
from resources.course import CreateCourse, FindCourses, UpdateCourse, DeleteCourse
from models import db
import os
from dotenv import load_dotenv

app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}})
# socketio = SocketIO(app, cors_allowed_origins="*")
load_dotenv()

# Configure your Flask app as before
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['CHAT_ENGINE_PRIVATE_KEY'] = os.environ.get('CHAT_ENGINE_PRIVATE_KEY')
app.config['CHAT_ENGINE_PROJECT_ID'] = os.environ.get('CHAT_ENGINE_PROJECT_ID')

CORS(app)
db.init_app(app)
api = Api(app)
jwt = JWTManager(app)
mail = Mail(app)
migrate = Migrate(app, db)

# Add resources to API
api.add_resource(Register, '/register', '/register/<int:id>')
api.add_resource(Login, '/learners-login')
api.add_resource(MessageResource, '/message', '/message/<int:message_id>')
api.add_resource(AdminLogin, '/admin-login')
api.add_resource(CreateCourse, '/courses')
api.add_resource(FindCourses, '/courses', '/courses/<int:course_id>')
api.add_resource(UpdateCourse, '/courses/<int:course_id>')
api.add_resource(DeleteCourse, '/courses/<int:course_id>')

if __name__ == '__main__':
    app.run(port=5555, debug=False)

# # REST API route
# @app.route('/http-call')
# def http_call():
#     data = {'data': 'This is a response from the server'}
#     return jsonify(data)

# # WebSocket events
# @socketio.on('connect')
# def connected():
#     print(request.sid)
#     print('client is connected')
#     emit("connected", {'data': f"id: {request.sid} is connected"})
    
# @socketio.on('disconnect')
# def disconnect():
#     print('client is disconnected')
#     emit("disconnect", f"user {request.sid} is disconnected", broadcast=True)
    
# @socketio.on('data')
# def handle_message(data):
#     print('Data from the front end: ', str(data))
#     emit('data', {'data': data, 'id': request.sid}, broadcast=True)

# if __name__ == '__main__':

#     # Run the application with both REST API and WebSocket support
#     socketio.run(app, debug=True, port=5555)

