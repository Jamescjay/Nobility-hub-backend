from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from resources.user import Register, Login, AdminLogin
from models import db
from resources.message import MessageResource 



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config["JWT_SECRET_KEY"] = "super-secret"
CORS(app)
db.init_app(app)
api = Api(app)
jwt = JWTManager(app)


# Add resources to API
api.add_resource(Register, '/register', '/register/<int:id>')
api.add_resource(Login, '/learners-login')
api.add_resource(MessageResource, '/message', '/message/<int:message_id>')
api.add_resource(AdminLogin, '/admin-login')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
