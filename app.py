from flask import Flask
from flask_migrate import Migrate
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
  return 'Hello world'