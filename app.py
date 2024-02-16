from flask import Flask
from flask_migrate import Migrate
from flask_restful import  Api
from flask_bcrypt import Bcrypt
from models import db
from resources.user import Register

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)
bcrypt = Bcrypt(app)

api.add_resource(Register, '/register')

if __name__ == '__main__':
    app.run(port=5555, debug=True)