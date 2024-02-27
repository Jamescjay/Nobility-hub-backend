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

class FindCourses(Resource):
    
    def get(self,course_id=None):
        if course_id:
            course = Course.query.get(course_id)
            if course:
                course_data = {
                    "id": course.id,
                    "title": course.title,
                    "phase" : course.phase,
                    "description" : course.description,
                    "course_url" : course.course_url,
                }
                return course_data, 200
            else:
                return {"message":"Course not Found"}, 400
        else:
            all_courses = Course.query.all()
            courses_data = [{
                "id": course.id,
                "title": course.title,
                "phase" : course.phase,
                "description" : course.description,
                "course_url" : course.course_url,
            }for course in all_courses]
            return courses_data, 200


    
        
class UpdateCourse(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title')
    parser.add_argument('phase', type=int)
    parser.add_argument('description')
    parser.add_argument('course_url')

    @marshal_with(response_field)
    def put(self, course_id):
        data = UpdateCourse.parser.parse_args()
        course = Course.query.get(course_id)
        if course:
            for key, value in data.items():
                if value is not None:
                    setattr(course, key, value)
            db.session.commit()
            return {"message":"Course updated successfully", "status":"success", "course":course}, 200
        else:
            return {"message":"Course not found", "status":"fail"},404

class DeleteCourse(Resource):
    def delete(self, course_id):
        course = Course.query.get(course_id)
        if course:
            db.session.delete(course)
            db.session.commit()
            return {"message":"Course deleted successfully", "status":"success"}, 200
        else:
            return {"message":"Course not found", "status":"fail"}, 404






