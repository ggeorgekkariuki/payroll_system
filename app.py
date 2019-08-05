# importing Flask class
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from config import *


# instantiating class Flask
app = Flask(__name__)

# config parameter that shows where our database lives
app.config.from_object(Development)
#app.config.from_object(Production)
#app.config.from_object(Testing)


#initialise SQLAlchemy app
db = SQLAlchemy(app)

from models.Departments import DepartmentModel
from models.Employees import EmployeeModel

# TODO: read about flask-migrate
@app.before_first_request
def create_tables():
    db.create_all()

# registering a route / routing
@app.route('/', methods=['GET'])
def index():
    departments = DepartmentModel.fetch_all()
    return render_template('index.html', departments=departments)

@app.route('/employees/<int:dept_id>')
def employees(dept_id):
    departments = DepartmentModel.fetch_all()
    employees = EmployeeModel.fetch_by_department(dept_id)
    this_dept = dept_id
    return render_template('employees.html', departments=departments, employees=employees, this_dept=this_dept)

@app.route('/payroll/<int:emp_id>')
def payrolls(emp_id):
    departments = DepartmentModel.fetch_all()
    employees = EmployeeModel.fetch_by_department(emp_id)
    return render_template('payrolls.html', departments=departments, employees=employees)

@app.route('/new_department', methods=['POST'])
def new_department():
    department_name =  request.form['department']
    if DepartmentModel.fetch_by_name(department_name):
        # read more on bootstrap alerts with flash
        flash('Department ' + department_name + ', already exists', 'danger')
        return redirect(url_for('index'))
    department = DepartmentModel(name=department_name)
    department.insert_to_db()
    flash('Department ' + department_name + ' has been added', 'success')
    return redirect(url_for('index'))

@app.route('/new_employee', methods=['POST'])
def new_employee():
    employee_name = request.form['name']
    gender = request.form['gender']
    kra_pin = request.form['kra_pin']
    national_id = request.form['national_id']
    email = request.form['email']
    basic_salary = request.form['basic_salary']
    benefits = request.form['benefits']
    dept_id = request.form['department']
    if EmployeeModel.fetch_by_mail(email):
        flash('Employee with the above details already exists', 'danger')
        return redirect(url_for('index'))
    employee = EmployeeModel(full_name = employee_name, gender = gender, kra_pin = kra_pin, email = email, national_id = national_id, basic_salary = basic_salary, benefits = benefits, department_id = dept_id)
    employee.insert_to_db()
    flash('Employee ' + employee_name + ' has been added', 'success')
    return redirect(url_for('index'))

@app.route('/department/edit/<int:dept_id>')
def edit_department(dept_id):
    pass

@app.route('/employee/edit/<int:emp_id>')
def edit_employee(emp_id):
    pass

@app.route('/department/delete/<int:dept_id>')
def delete_department(dept_id):
    pass

@app.route('/employee/edit/<int:emp_id>')
def delete_employee(emp_id):
    pass


# Run flask app
if __name__ == '__main__':
    app.run()
