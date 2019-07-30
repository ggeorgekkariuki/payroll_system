# importing Flask class
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Development, Testing


# instantiating class Flask
app = Flask(__name__)

# config parameter that shows where our database lives
app.config.from_object(Development)
# app.config.from_object('Testing')

#initialise SQLAlchemy app
db = SQLAlchemy(app)

from models.Departments import DepartmentModel
from models.Employees import EmployeeModel

@app.before_first_request
def create_tables():
    db.create_all()

# registering a route / routing
@app.route('/')
# function to run when clients visit this route
def hello_world():
    return render_template('index.html')

@app.route('/name')
def name():
    return 'Keith'

# Run flask app
# if __name__ == '__main__':
#      app.run()
