import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

# The func helper from sqlalchemy.sql accesses SQLfunctions.
# Needed to set a default creation date and time for when a student record is created

from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# SQLALCHEMY_DATABASE_URI: The database URI to specify the database you want to establish a connection with

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')

# SQLALCHEMY_TRACK_MODIFICATIONS: A configuration to enable or disable tracking modifications of objects. You set it to False to disable tracking and use less memory.        
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Database table for students, which is represented by a model - A python class that inherits from a base class Flask-SQLAlchemy

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    bio = db.Column(db.Text)


    # The special __repr__ function allows you to give each object a string representation to recognize it for debugging purposes.
    #  In this case you use the student’s first name.

    def __repr__(self):
        return f'<Student {self.firstname}>'



# you create an index() view function using the app.route() decorator.
# In this function, you query the database and get all the students using the Student model with the query attribute, 
# which allows you to retrieve one or more items from the database using different methods.
# You use the all() method to get all student entries in the database. You store the query result in a variable called students 
# and pass it to a template called index.html that you render using the render_template() helper function.
@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)



# To retrieve a student by their ID, you’ll create a new route that renders a page for each individual student
# The get_or_404() method is a get() variant. get() only returns 'None'
# Whilst the get_or_404() returns '404 Not Found' HTTP response

@app.route('/<int:student_id>/')
def student(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('student.html', student=student)


# When the user first requests the /create route using a GET request,
# ... a template file called create.html will be rendered.
# The if condition below handles POST requests
@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == "POST":
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        age = int(request.form['age'])
        bio = request.form['bio']
        student = Student(firstname=firstname,
                          lastname=lastname,
                          email=email,
                          age=age,
                          bio=bio)
        db.session.add(student)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('create.html')


# ...


@app.route('/<int:student_id>/edit/', methods=('GET', 'POST'))
def edit(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        age = int(request.form['age'])
        bio = request.form['bio']

        student.firstname = firstname
        student.lastname = lastname
        student.email = email
        student.age = age
        student.bio = bio

        db.session.add(student)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('edit.html', student=student)



# ...

@app.post('/<int:student_id>/delete/')
def delete(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))