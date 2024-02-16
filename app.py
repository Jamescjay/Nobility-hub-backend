from flask import Flask
from flask_migrate import Migrate
from flask_restful import  Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from models import db
from resources.user import Register, Login

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config["JWT_SECRET_KEY"] = "super-secret" 

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

api.add_resource(Register, '/register')
api.add_resource(Login, '/login')

if __name__ == '__main__':
    app.run(port=5555, debug=True)