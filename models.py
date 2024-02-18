from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ ="user"

    id= db.Column(db.Integer, primary_key=True)
    first_name=db.Column(db.String(25), nullable=False)
    last_name=db.Column(db.String(25), nullable=False)
    username=db.Column(db.String(25), nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    phone = db.Column(db.String, nullable=False, unique=True)
    role = db.Column(db.Text, nullable=False)
    gender = db.Column(db.Text, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())
    updated_at = db.Column(db.TIMESTAMP, onupdate=db.func.now())

# class Authentication(db.Model):
#     __tablename__ ="authentication"
#     id= db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String, nullable=False, unique=True)
#     password = db.Column(db.String, nullable=False)
#     created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())