from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'

db = SQLAlchemy(app)


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)


@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)


@app.route('/create', methods=['GET', 'POST'])
def create():

    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')

        student = Student(name=name, age=age)

        db.session.add(student)
        db.session.commit()

        return redirect('/')

    return render_template('create.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
