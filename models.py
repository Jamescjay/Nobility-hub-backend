from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ ="user"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    username = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    phone = db.Column(db.String, nullable=False, unique=True)
    role = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())
    updated_at = db.Column(db.TIMESTAMP, onupdate=db.func.now())

    messages_sent = relationship("Message", back_populates="sender", foreign_keys='Message.sender_id')
    messages_received = relationship("Message", back_populates="recipient", foreign_keys='Message.recipient_id')

class Message(db.Model):
    __tablename__ = "message"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.TIMESTAMP(timezone=True), default=datetime.utcnow)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, name='fk_message_sender_id')
    recipient_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, name='fk_message_recipient_id')

    sender = relationship("User", back_populates="messages_sent", foreign_keys=[sender_id])
    recipient = relationship("User", back_populates="messages_received", foreign_keys=[recipient_id])

class Course(db.Model):
    __tablename__ = "course"

    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(120), nullable=False)
    phase=db.Column(db.Integer, nullable=False)
    description=db.Column(db.Text, nullable=False)
    course_url=db.Column(db.String, nullable=False)