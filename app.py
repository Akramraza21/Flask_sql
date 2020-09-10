from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
import datetime
import json


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db'
db = SQLAlchemy(app)


class Student(db.Model):
    # db structure is like putting Name, roll number, date, presence
    # all the data recordes

    id = db.Column(db.Integer, primary_key=True)
    studentName = db.Column(db.String(50), nullable=False)
    rollNo = db.Column(db.Text, default='N/A')
    date = db.Column(db.Text, nullable=False)
    presence = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return 'Student ' + str(self.id)


# class Attendence(db.Model):
#     # db Attendence is like putting presence or absence of student

#     id = db.Column(db.Integer, primary_key=True)
#     rollNo = db.Column(db.Text, default='N/A')
#     presence = db.Column(db.String(10), nullable=False)

#     def __repr__(self):
#         return 'Student Attendence ' + str(self.id)


class ShowAttendence(Resource):
    #  getting data from api
    def get(self):
        students = Student.query.all()
        studentsdata = []
        for student in students:
            studentis = {}
            studentis["name"] = student.studentName
            studentis["rollNo"] = student.rollNo
            studentis["date"] = student.date
            studentis["presence"] = student.presence
            if len(studentsdata) >= 10:
                break
            else:
                studentsdata.append(studentis)
        # print('_______________________________', studentsdata)
        return jsonify(studentsdata)

    def post(self):
        # use rollNo to fetch total attendence

        data = request.get_json()
        rollNumber = data['rollNo']
        count = 0
        name = None
        data = Student.query.all()
        for value in data:
            # print('____________________', type(value.rollNo), type(rollNumber))
            if value.rollNo == str(rollNumber):
                count += 1
        if count:
            student = Student.query.get(rollNumber)
        return {"name": student.studentName, "rollNo": rollNumber, "total present": str(count)}


class AddPresence(Resource):
    # use roll number and presence while posting
    def post(self):
        fromPostman = request.get_json()
        fromDatabase = Student.query.all()
        rollNo = fromPostman['rollNo']
        presence = None
        presence = fromPostman['presence']
        if rollNo:
            data = Student.query.get(rollNo)
            added = Student(studentName=data.studentName,
                            rollNo=data.rollNo, presence=data.presence, date=datetime.datetime.now())
            db.session.add(added)
            db.session.commit()
            return 'attendence is recorded'

        '''
        ###### this set of code is used to add extra student to the database 
        student = request.get_json()  # data from postmanor ui
        print('_____________________________', student["name"])
        sessionIs = Student(
            studentName=student["name"], rollNo=student["rollNo"], date=student["date"], presence=student["presence"])
        db.session.add(sessionIs)
        db.session.commit()
        return 'done'
        '''


# route is '/' for get and '/attendence' for post


api.add_resource(ShowAttendence, '/')
api.add_resource(AddPresence, '/attendence')


if __name__ == "__main__":
    app.run(debug=True, port=5001)
