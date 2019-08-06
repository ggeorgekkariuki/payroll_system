from app import db
from models.Employees import EmployeeModel

class PayrollModel(db.Model):
    __tablename__ = 'payrolls'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50))
    month = db.Column(db.String(20))
    overtime = db.Column(db.Float)
    loan_deduction = db.Column(db.Float)
    salary_advance = db.Column(db.Float)
    gross_salary = db.Column(db.Float)
    NSSF = db.Column(db.Float)
    taxable_income = db.Column(db.Float)
    PAYE = db.Column(db.Float)
    personal_relief = db.Column(db.Float)
    tax_net_off_relief = db.Column(db.Float)
    NHIF = db.Column(db.Float)
    net_salary = db.Column(db.Float)
    take_home_pay = db.Column(db.Float)
    # Defining the Foreign Key for the departments Table
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    employee = db.relationship('EmployeeModel', backref=db.backref("payrolls", single_parent=True, lazy=True))

    def insert_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def fetch_by_employee(cls, emp_id):
        return cls.query.filter_by(employee_id=emp_id)