from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy


# creating an instance of flask
app = Flask(__name__)
app.app_context().push()

# creating an API object
api = Api(app)

# creating database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db'
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False

#SQLALCHEMY Mapping
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    index_number = db.Column(db.String(80), nullable=False)
    
    def __repr__(self):
        return f"{self.firstname} - {self.lastname} - {self.gender} - {self.age} - {self.index_number}"
    


# For GET request to http://localhost:5000/api/get_records
class GetStudents(Resource):
    def get(self):
        students = Student.query.all()
        student_list = []
        
        for student in students:
            student_data = {
                'Id': student.id, 'Firstname': student.firstname, 'Lasttname': student.lastname, 'Gender': student.gender,
                'Age': student.age, 'IndexNumber': student.index_number
            }
            student_list.append(student_data)
            
        return {"Students": student_list}, 200
    
        
        
# For Post request to http://localhost:5000/api/create_record
class CreateStudent(Resource):
    def post(self):
        if request.is_json:
            student = Student(firstname=request.json['Firstname'], lastname=request.json['Lastname'], gender=request.json['Gender'],
                              age=request.json['Age'], index_number=request.json['IndexNumber'])
            db.session.add(student)
            db.session.commit()
            
            # return a json response
            return make_response(jsonify({
                'Id': student.id, 'Firstname': student.firstname, 'Lasttname': student.lastname, 'Gender': student.gender,
                'Age': student.age, 'IndexNumber': student.index_number}), 201)
        else:
            return {'error': 'Request must be JSON'}, 400
        

# For Post request to http://localhost:5000/api/update_record/?
class UpdateStudent(Resource):
    def put(self, id):
        if request.is_json:
            student = Student.query.get(id)
            if student is None:
                return {'error': 'not found'}, 404
            else:
                student.firstname = request.json['Firstname']
                student.lastname = request.json['Lastname']
                student.gender = request.json['Gender']
                student.index_number = request.json['IndexNumber']
                db.session.commit()
                return 'Updated', 200
        else:
            return {'error': 'Request must be JSON'}, 400


# For GET request to http://localhost:5000/api/get_record/<id> for a particular student        
class StudentDetail(Resource):
    def get(self, student_id):
        student = Student.query.get_or_404(student_id)
        return student.__repr__()
            


api.add_resource(GetStudents, '/api/get_records')
api.add_resource(StudentDetail, '/api/get_record/<int:student_id>')
api.add_resource(CreateStudent, '/api/create_record')
api.add_resource(UpdateStudent, '/api/update_record/<int:id>')




if __name__ == '__main__':
    app.run(debug=True)