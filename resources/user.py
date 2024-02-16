from flask_restful import Resource, reqparse, fields, marshal_with
from flask_bcrypt import generate_password_hash, check_password_hash
from models import User, db

user_fields={
    "id":fields.Integer,
    "username":fields.String,
    "first_name":fields.String,
    "last_name":fields.String,
    "email":fields.String,
    "gender":fields.String,
    "role":fields.String,
    "phone":fields.Integer,
    "created_at":fields.DateTime,
    "updated_at":fields.DateTime
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
    data=Register.parser.parse_args()

    data['password']=generate_password_hash(data['password'])
    data['role'] = 'learner'
    user = User(**data)

    email=User.query.filter_by(email=data['email']).one_or_none()
    if email:
      return {"message":"email already taken", "status": "fail"}, 400
    phone = User.query.filter_by(phone = data['phone']).one_or_none()

    if phone:
      return {"message":"Phone number already exists", "status": "fail"}, 400


    try:
      db.session.add(user)
      db.session.commit()
      db.session.refresh(user)

      return {"message": "Account created successfully", "status": "success", "user": user}
    except:
      return {"message": "Unable to create account", "status": "fail"}