# importing Flask class
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from config import *
from resources.calculator import KRACalculator as Payroll
import pygal


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
    all_employees = EmployeeModel.fetch_all()
    male = 0
    female = 0
    others = 0
    for employee in all_employees:
        if employee.gender == 'm':
            male += 1
        elif employee.gender == 'f':
            female += 1
        else:
            others += 1

    pie_chart = pygal.Pie()
    pie_chart.title = 'Comparing company employees by gender'
    pie_chart.add('Male', male)
    pie_chart.add('Female', female)
    pie_chart.add('Others', others)
    pie_graph = pie_chart.render_data_uri()

    line_chart = pygal.Bar()
    line_chart.title = 'Salary cost per department'
    for department in departments:
        line_chart.add(department.name, DepartmentModel.fetch_total_payroll_department_id(department.id))

    line_graph = line_chart.render_data_uri()
    return render_template('index.html', departments=departments, pie_graph=pie_graph, line_graph=line_graph)

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
    return redirect(url_for('payrolls',emp_id=this_employee.id))

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

@app.route('/edit_department/<int:dept_id>', methods=['POST'])
def edit_department(dept_id):
    department_name = request.form['department']
    DepartmentModel.update_department(id=dept_id, name=department_name)

    flash('Department ' + department_name + ' has been updated', 'success')
    return redirect(url_for('index'))

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

@app.route('/edit_payslip/<int:pay_id>', methods=['POST'])
def edit_payslip(pay_id):
    this_payslip = PayrollModel.fetch_payslip_by_id(pay_id)
    this_employee = this_payslip.employee

    overtime = request.form['overtime']
    payroll = Payroll(this_employee.full_name, this_employee.basic_salary, this_employee.benefits, float(overtime))
    name = payroll.name
    month = request.form['month']
    loan = request.form['loan']
    salary_advance = request.form['salary_advance']
    gross_salary = payroll.gross_salary
    taxable_income = payroll.taxable_income
    nssf = round(payroll.NSSF, 2)
    paye = round(payroll.PAYE, 2)
    personal_relief = payroll.personal_relief
    tax_net_off_relief = round(payroll.after_relief, 2)
    nhif = payroll.NHIF
    net_salary = round(payroll.net_salary, 2)
    take_home_pay = net_salary - (float(loan) + float(salary_advance))

    PayrollModel.update_payslip(id=pay_id, full_name=name, month=month, overtime=overtime, loan_deduction=loan, salary_advance=salary_advance, gross_salary=gross_salary, NSSF=nssf, PAYE=paye, personal_relief=personal_relief, tax_net_off_relief=tax_net_off_relief, NHIF=nhif,net_salary=net_salary, take_home_pay=take_home_pay)

    return redirect(url_for('payrolls', emp_id=this_employee.id))

@app.route('/delete_employee/<int:emp_id>')
def delete_employee(emp_id):
    this_emp = EmployeeModel.fetch_employee_by_id(emp_id)
    this_dept = this_emp.department

    EmployeeModel.delete_by_id(emp_id)
    flash('Employee has been deleted', 'success')
    return redirect(url_for('employees', dept_id=this_dept.id))

@app.route('/delete_department/<int:dept_id>')
def delete_department(dept_id):
    DepartmentModel.delete_by_id(dept_id)
    flash('Department has been deleted', 'success')
    return redirect(url_for('index'))

@app.route('/delete_payslip/<int:pay_id>')
def delete_payslip(pay_id):
    this_payslip = PayrollModel.fetch_payslip_by_id(pay_id)
    this_employee = this_payslip.employee
    PayrollModel.delete_by_id(pay_id)
    flash('Payslip has been deleted', 'success')
    return redirect(url_for('payrolls', emp_id=this_employee.id))

# Run flask app
if __name__ == '__main__':
    app.run()
