# from flask import Flask, jsonify, request
# app = Flask(__name__)
# students = []
# @app.route("/")
# def Home():
#     return "WELCOME TO FLASK SESSION"

# @app.route('/hello')
# def hello():
#     return " HELLO, Batch10"

# ## BASIC CRUD OPS 
# ## SCHOOL MANAGEMENT SYSTEM -- list-students, add a students, delete a student
# # listing all students
# @app.route('/students',methods=['GET'])
# def list_students():
#     return jsonify(students)
# # add students to student list
# @app.route('/students',methods=['POST'])
# def add_student():
#     data = request.get_json()
#     students.append(data)   # students = [] -- add one student(a) -- append -- students = [a]
#     return jsonify({"msg" : "student Added"})

# # Delete student
# #  "/student/<int:id>" -- path parameter -- 
# @app.route("/student/<int:id>",methods=['Delete'])
# def delete_student(id):
#     if 0<=id<len(students):  # id > = 0 id < students list length
#         removed = students.pop(id)
#         return jsonify({"msg":"student deleted"})
#     else:
#         return jsonify({"error":"Invalid ID"})


# if __name__ == '__main__':
#     app.run(debug=True)

# # Books APIS
# # books = []
# # books = [{"title":"abc","author":"xyz","year":2025}]
# # create get post and delete api respectively

from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from models import db, Student
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
api = Api(app)

# Flask CLI command to create DB tables
@app.cli.command("create_db")
def create_db():
    db.create_all()
    print("Database tables created!")

# CRUD Resources
class StudentListResource(Resource):
    def get(self):
        students = Student.query.all()
        return jsonify([s.to_dict() for s in students])

    def post(self):
        data = request.get_json()
        new_student = Student(name=data["name"], age=data["age"], grade=data["grade"])
        db.session.add(new_student)
        db.session.commit()
        return jsonify(new_student.to_dict())

class StudentResource(Resource):
    def get(self, student_id):
        student = Student.query.get_or_404(student_id)
        return jsonify(student.to_dict())

    def put(self, student_id):
        student = Student.query.get_or_404(student_id)
        data = request.get_json()
        student.name = data.get("name", student.name)
        student.age = data.get("age", student.age)
        student.grade = data.get("grade", student.grade)
        db.session.commit()
        return jsonify(student.to_dict())

    def delete(self, student_id):
        student = Student.query.get_or_404(student_id)
        db.session.delete(student)
        db.session.commit()
        return jsonify({"message": "Student deleted"})

# API routes
api.add_resource(StudentListResource, "/school/students")
api.add_resource(StudentResource, "/school/students/<int:student_id>")

def hello():
    return " hi "

def hi():
    return "hello"


def switch():
    return "switched"

if __name__ == "__main__":
    app.run(debug=True)


