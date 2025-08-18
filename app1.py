from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from models import db, Student
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.config["JWT_SECRET_KEY"] = "supersecretjwtkey"  # For JWT signing

db.init_app(app)
api = Api(app)
jwt = JWTManager(app)

# Dummy user for example
USERS = {"admin": "password123"}

@app.cli.command("create_db")
def create_db():
    db.create_all()
    print("Database tables created!")

# Login route
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if USERS.get(username) == password:
        token = create_access_token(identity=username)
        return jsonify({"access_token": token})
    return jsonify({"error": "Invalid credentials"}), 401

# CRUD Resources
class StudentListResource(Resource):
    @jwt_required()
    def get(self):
        students = Student.query.all()
        return jsonify([s.to_dict() for s in students])

    @jwt_required()
    def post(self):
        data = request.get_json()
        new_student = Student(name=data["name"], age=data["age"], grade=data["grade"])
        db.session.add(new_student)
        db.session.commit()
        return jsonify(new_student.to_dict())

class StudentResource(Resource):
    @jwt_required()
    def get(self, student_id):
        student = Student.query.get_or_404(student_id)
        return jsonify(student.to_dict())

    @jwt_required()
    def put(self, student_id):
        student = Student.query.get_or_404(student_id)
        data = request.get_json()
        student.name = data.get("name", student.name)
        student.age = data.get("age", student.age)
        student.grade = data.get("grade", student.grade)
        db.session.commit()
        return jsonify(student.to_dict())

    @jwt_required()
    def delete(self, student_id):
        student = Student.query.get_or_404(student_id)
        db.session.delete(student)
        db.session.commit()
        return jsonify({"message": "Student deleted"})

api.add_resource(StudentListResource, "/students")
api.add_resource(StudentResource, "/students/<int:student_id>")

if __name__ == "__main__":
    app.run(debug=True)
