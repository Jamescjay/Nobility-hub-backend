from flask_restful import Resource, reqparse, marshal_with, fields
from models import db, Message, User
from datetime import datetime

message_fields = {
    'id': fields.Integer,
    'content': fields.String,
    'timestamp': fields.DateTime,
    'sender': fields.Nested({
        'id': fields.Integer,
        'username': fields.String,
    }),
}

message_put_args = reqparse.RequestParser()
message_put_args.add_argument('sender', type=str, help='Sender username is required', required=True)
message_put_args.add_argument('content', type=str, help='Content of the message is required', required=True)

class MessageResource(Resource):
    @marshal_with(message_fields)
    def get(self, message_id):
        message = Message.query.get(message_id)
        if message:
            return message
        else:
            return {'message': 'Message not found'}, 404

    @marshal_with(message_fields)
    def put(self, message_id):
        args = message_put_args.parse_args()
        message = Message.query.get(message_id)
        if message:
            message.content = args['content']
            message.timestamp = datetime.utcnow()
            db.session.commit()
            return message
        else:
            return {'message': 'Message not found'}, 404

    @marshal_with(message_fields)
    def post(self):
        args = message_put_args.parse_args()
        sender_username = args['sender']
        sender = User.query.filter_by(username=sender_username).first()
        if not sender:
            return {'message': 'Sender not found'}, 404

        message = Message(content=args['content'], sender=sender)
        db.session.add(message)
        db.session.commit()
        return message, 201

    @marshal_with(message_fields)
    def delete(self, message_id):
        message = Message.query.get(message_id)
        if message:
            db.session.delete(message)
            db.session.commit()
            return {'message': 'Message deleted successfully'}, 200
        else:
            return {'message': 'Message not found'}, 404