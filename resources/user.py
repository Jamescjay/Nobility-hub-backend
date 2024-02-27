from flask_restful import Resource, reqparse, fields, marshal_with
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_bcrypt import generate_password_hash, check_password_hash
from models import User, db
from flask import request
from flask_mail import Message

user_fields = {
    "id": fields.Integer,
    "username": fields.String,
    "first_name": fields.String,
    "last_name": fields.String,
    "email": fields.String,
    "gender": fields.String,
    "role": fields.String,
    "phone": fields.Integer,
    "created_at": fields.DateTime,
    "updated_at": fields.DateTime
}

response_field = {
    "message": fields.String,
    "status": fields.String,
    "user": fields.Nested(user_fields)
}

class Register(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('first_name', required=True, help="first_name is required")
    parser.add_argument('last_name', required=True, help="last_name is required")
    parser.add_argument('phone', required=True, help="Phone number is required")
    parser.add_argument('email', required=True, help="Email address is required")
    parser.add_argument('password', required=True, help="Password is required")
    parser.add_argument('username', required=True, help="username is required")
    parser.add_argument('gender', required=True, help="gender is required")

    @marshal_with(response_field)
    def post(self):
        from app import mail

        data = Register.parser.parse_args()
        user_password = data['password']
        data['password'] = generate_password_hash(data['password'])
        data['role'] = 'learner'
        user = User(**data)

        email = User.query.filter_by(email=data['email']).one_or_none()
        if email:
            return {"message": "email already taken", "status": "fail"}, 400

        phone = User.query.filter_by(phone=data['phone']).one_or_none()
        if phone:
            return {"message": "Phone number already exists", "status": "fail"}, 400

        try:
            db.session.add(user)
            db.session.commit()

            
            msg = Message('Confirmation Email', sender='nobilityhub@gmail.com', recipients=[data['email']])
            msg.body = f"Dear {data['first_name']},\n\nYour account has been successfully registered. Your password is: {user_password}\n\nPlease click on the following link to confirm your email: http://localhost:3000"
            mail.send(msg)

            return {"message": "Account created successfully", "status": "success", "user": user}, 201
        except Exception as e:
            return {"message": str(e), "status": "fail"}, 400

    def get(self, id=None):
        if id:
            user = User.query.get(id)
            if user:
                user_data = {
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "gender": user.gender,
                    "role": user.role,
                    "phone": user.phone,
                    "created_at": user.created_at.isoformat() if user.created_at else None,
                    "updated_at": user.updated_at.isoformat() if user.updated_at else None
                }
                return user_data, 200
            else:
                return {"message": "User not found"}, 404
        else:
            users = User.query.all()
            users_data = [{
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "gender": user.gender,
                "role": user.role,
                "phone": user.phone,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "updated_at": user.updated_at.isoformat() if user.updated_at else None
            } for user in users]
            return users_data, 200




class Login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', required=True, help="Email is required")
    parser.add_argument('password', required=True, help="Password is required")

    def post(self):
      data = Login.parser.parse_args()
      user = User.query.filter_by(email = data['email']).first()

      if user:
        is_password_correct = check_password_hash(user.password, data['password'])

        if is_password_correct:
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(user.id)

            return {"message": "Login successfully","access_token": access_token, "refresh_token": refresh_token, "status": "success", "id": user.id}, 200

        else:
          return {"message": "Invalid email/password", "status": "fail"}, 403
      else:
        return {"message": "Invalid email/password", "status": "fail"}, 403
      
class AdminLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', required=True, help="Email is required")
    parser.add_argument('password', required=True, help="Password is required")

    def post(self):
        data = AdminLogin.parser.parse_args()

        # Admin credentials to the system
        admin_credentials = {
            'nobilityhub@gmail.com': 'password'
        }

        if data['email'] in admin_credentials and data['password'] == admin_credentials[data['email']]:
            access_token = create_access_token(identity=data['email'])
            refresh_token = create_refresh_token(data['email'])
            return {"message": "Admin login successfully", "access_token": access_token, "refresh_token": refresh_token, "status": "success"}, 200
        else:
            return {"message": "Invalid email/password for admin", "status": "fail"}, 403