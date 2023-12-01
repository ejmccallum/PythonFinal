from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

mongo_client = MongoClient("mongodb+srv://ejmccallum:7ab9i8j39_FA%21i2@cluster0.xp3m8g3.mongodb.net/")
db = mongo_client.Gradebook

subjects = ["History", "Mathematics", "Literacy", "Science"]

@app.route('/')
def index():
    return render_template('index.html', subjects=subjects)

@app.route('/<subject>/grades')
def subject_grades(subject):
    collection = db[subject]
    data = collection.find()
    return render_template('subject_grades.html', subject=subject, data=data)

@app.route('/<subject>')
def subject_detail(subject):
    return render_template('subject_detail.html', subject=subject)

@app.route('/<subject>/add', methods=['POST'])
def add_entry(subject):
    collection = db[subject]
    student = request.form['student']
    assignment = request.form['assignment']
    grade = request.form['grade']
    teacher = request.form['teacher']

    entry = {
        'student_name': student,
        'assignment_name': assignment,
        'grade_value': grade,
        'teacher_name': teacher
    }

    collection.insert_one(entry)
    
    # Use url_for to generate the correct URL for 'subject_grades'
    return redirect(url_for('subject_grades', subject=subject))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5555)
