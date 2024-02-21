from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ ="user"

    id= db.Column(db.Integer, primary_key=True)
    first_name=db.Column(db.String(25), nullable=False)
    last_name=db.Column(db.String(25), nullable=False)
    username=db.Column(db.String(25), nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    phone = db.Column(db.String, nullable=False, unique=True)
    role = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())
    updated_at = db.Column(db.TIMESTAMP, onupdate=db.func.now())

    messages = relationship("Message", back_populates="sender")

class Message(db.Model):
    __tablename__ = "message"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.TIMESTAMP(timezone=True), default=datetime.utcnow)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    sender = relationship("User", back_populates="messages")