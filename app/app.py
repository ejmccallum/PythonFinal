from flask import Flask, render_template, request, redirect, url_for, Response
from pymongo import MongoClient
from bson.objectid import ObjectId
from typing import Any, Dict
from pymongo.collection import Collection

app = Flask(__name__)

mongo_client = MongoClient(
    "mongodb+srv://ejmccallum:7ab9i8j39_FA%21i2@cluster0.xp3m8g3.mongodb.net/")
db = mongo_client.Gradebook

subjects = ["History", "Mathematics", "Literacy", "Science"]


@app.route('/')
def index() -> Response:
    return render_template('index.html', subjects=subjects)


@app.route('/<subject>/grades')
def subject_grades(subject: str) -> Response:
    collection: Collection = db[subject]
    data = collection.find()
    return render_template('subject_grades.html', subject=subject, data=data)


@app.route('/<subject>')
def subject_detail(subject: str) -> Response:
    return render_template('subject_detail.html', subject=subject)


@app.route('/<subject>/add', methods=['POST'])
def add_entry(subject: str) -> Response:
    collection: Collection = db[subject]
    student: str = request.form['student']
    assignment: str = request.form['assignment']
    grade: str = request.form['grade']
    teacher: str = request.form['teacher']

    entry: Dict[str, Any] = {
        'student_name': student,
        'assignment_name': assignment,
        'grade_value': grade,
        'teacher_name': teacher
    }

    collection.insert_one(entry)
    return redirect(url_for('subject_grades', subject=subject))


@app.route('/<subject>/edit/<entry_id>', methods=['GET', 'POST'])
def edit_entry(subject: str, entry_id: str) -> Response:
    collection: Collection = db[subject]
    entry = collection.find_one({'_id': ObjectId(entry_id)})

    if request.method == 'POST':
        # Update the entry with the edited values
        updated_entry = {
            'student_name': request.form['student'],
            'assignment_name': request.form['assignment'],
            'grade_value': request.form['grade'],
            'teacher_name': request.form['teacher']
        }
        collection.update_one({'_id': ObjectId(entry_id)},
                              {'$set': updated_entry})
        return redirect(url_for('subject_grades', subject=subject))

    return render_template('edit_entry.html', subject=subject, entry=entry)


@app.route('/<subject>/delete/<entry_id>', methods=['POST'])
def delete_entry(subject: str, entry_id: str) -> Response:
    collection: Collection = db[subject]
    collection.delete_one({'_id': ObjectId(entry_id)})
    return redirect(url_for('subject_grades', subject=subject))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5555)
