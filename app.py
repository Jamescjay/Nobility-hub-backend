from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail, Message
from resources.user import Register, Login, AdminLogin
from models import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'nobilityhub@gmail.com'
app.config['MAIL_PASSWORD'] = 'orcvtwyqejxejigv'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

CORS(app)
db.init_app(app)
api = Api(app)
jwt = JWTManager(app)
mail = Mail(app)
migrate = Migrate(app, db)

# Add resources to API
api.add_resource(Register, '/register', '/register/<int:id>')
api.add_resource(Login, '/learners-login')
api.add_resource(AdminLogin, '/admin-login')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
