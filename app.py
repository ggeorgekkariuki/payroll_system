# importing Flask class
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from config import *
from resources.calculator import KRACalculator as Payroll


# instantiating class Flask
app = Flask(__name__)

# config parameter that shows where our database lives
#app.config.from_object(Development)
app.config.from_object(Production)
#app.config.from_object(Testing)


#initialise SQLAlchemy app
db = SQLAlchemy(app)

from models.Departments import DepartmentModel
from models.Employees import EmployeeModel
from models.Payrolls import PayrollModel

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
    this_department = DepartmentModel.fetch_by_department(dept_id)
    departments = DepartmentModel.fetch_all()
    return render_template('employees.html', this_department=this_department, departments=departments)

@app.route('/payroll/<int:emp_id>')
def payrolls(emp_id):
    employee = EmployeeModel.fetch_employee_by_id(emp_id)
    payslips = PayrollModel.fetch_by_employee(emp_id)
    return render_template('payrolls.html', employee=employee, payslips=payslips )

@app.route('/generate_payroll/<int:emp_id>', methods=['POST'])
def generate_payroll(emp_id):
    this_employee = EmployeeModel.fetch_employee_by_id(emp_id)
    overtime = request.form['overtime']

    payroll = Payroll(this_employee.full_name, this_employee.basic_salary, this_employee.benefits, float(overtime))

    name = payroll.name
    month = request.form['month']
    loan = request.form['loan']
    salary_advance = request.form['salary_advance']
    gross_salary =  payroll.gross_salary
    taxable_income = payroll.taxable_income
    nssf =  round(payroll.NSSF, 2)
    paye =  round(payroll.PAYE, 2)
    personal_relief = payroll.personal_relief
    tax_net_off_relief =  round(payroll.after_relief, 2)
    nhif =  payroll.NHIF
    net_salary =  round(payroll.net_salary, 2)
    take_home_pay = net_salary - (float(loan)  + float(salary_advance))

    payslip = PayrollModel(full_name=name, month=month, overtime=overtime,loan_deduction=loan, salary_advance=salary_advance, gross_salary=gross_salary, NSSF=nssf, taxable_income=taxable_income, PAYE=paye, personal_relief=personal_relief, tax_net_off_relief=tax_net_off_relief, NHIF=nhif, net_salary=net_salary, take_home_pay=take_home_pay, employee_id=this_employee.id)
    payslip.insert_to_db()
    flash('Payslip for ' + this_employee.full_name + ' has been successfully generated', 'success')
    return redirect(url_for('index'))

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

@app.route('/edit_employee/<int:emp_id>', methods=['POST'])
def edit_employee(emp_id):


    employee_name = request.form['name']
    gender = request.form['gender']
    kra_pin = request.form['kra_pin']
    national_id = request.form['national_id']
    email = request.form['email']
    basic_salary = request.form['basic_salary']
    benefits = request.form['benefits']
    dept_id = int(request.form['department'])

    if gender == '0':
        gender = None
    if dept_id == 0:
        dept_id = None

    EmployeeModel.update_employee(id=emp_id, full_name=employee_name, gender=gender, kra_pin=kra_pin, email=email, national_id=national_id, basic_salary=basic_salary, benefits=benefits, department_id=dept_id)
    flash('Employee ' + employee_name + ' has been updated', 'success')

    this_emp = EmployeeModel.fetch_employee_by_id(emp_id)
    this_dept = this_emp.department
    return redirect(url_for('employees', dept_id=this_dept.id))

@app.route('/delete_employee/<int:emp_id>')
def delete_employee(emp_id):
    this_emp = EmployeeModel.fetch_employee_by_id(emp_id)
    this_dept = this_emp.department

    EmployeeModel.delete_by_id(emp_id)
    flash('Employee has been deleted', 'success')
    return redirect(url_for('employees', dept_id=this_dept.id))



# Run flask app
if __name__ == '__main__':
    app.run()
