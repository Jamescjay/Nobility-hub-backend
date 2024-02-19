from flask_restful import fields, Resource, reqparse, marshal_with
from models import db, Course

course_fields = {
    "id": fields.Integer,
    "title": fields.String,
    "phase" : fields.Integer,
    "description" : fields.String,
    "course_url" : fields.String,
    # "cohort_id" : fields.Integer
}

response_field = {
    "message" : fields.String,
    "status" : fields.String,
    "course" : fields.Nested(course_fields)
}

class CreateCourse(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', required=True, help='Title is required')
    parser.add_argument('phase',type=int, required=True, help='Phase No. is required')
    parser.add_argument('description', required=True, help='Description is required')
    parser.add_argument('course_url', required=True, help='Course_url is required')
    # parser.add_argument('cohort_id', type=int, required=True, help='Cohort is required')

    @marshal_with(response_field)
    def post(self):
        data = CreateCourse.parser.parse_args()

        course = Course(**data)

        db.session.add(course)
        db.session.commit()

        return {"message":"Created Course successfully", "status":"success", "course":course}, 201
    



