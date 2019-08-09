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
    employee = db.relationship('EmployeeModel', backref=db.backref("payrolls", single_parent=True, lazy=True, cascade='all,delete'))

    def insert_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def fetch_by_employee(cls, emp_id):
        return cls.query.filter_by(employee_id=emp_id)

    @classmethod
    def fetch_payslip_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def update_payslip(cls, id, full_name=None, month=None, overtime=None, loan_deduction=None, salary_advance=None, gross_salary=None,NSSF=None, taxable_income=None, PAYE=None, personal_relief=None, tax_net_off_relief=None, NHIF=None, net_salary=None, take_home_pay=None):
        record = cls.fetch_payslip_by_id(id)

        if full_name:
            record.full_name=full_name
        if month:
            record.month=month
        if overtime:
            record.overtime=overtime
        if loan_deduction:
            record.loan_deduction=loan_deduction
        if salary_advance:
            record.salary_advance=salary_advance
        if gross_salary:
            record.gross_salary=gross_salary
        if NSSF:
            record.NSSF=NSSF
        if taxable_income:
            record.taxable_income=taxable_income
        if PAYE:
            record.PAYE=PAYE
        if personal_relief:
            record.personal_relief=personal_relief
        if tax_net_off_relief:
            record.tax_net_off_relief=tax_net_off_relief
        if NHIF:
            record.NHIF=NHIF
        if net_salary:
            record.net_salary=net_salary
        if take_home_pay:
            record.take_home_pay=take_home_pay

        db.session.commit()
        return True



    @classmethod
    def delete_by_id(cls, id):
        record = cls.query.filter_by(id=id)
        record.delete()
        db.session.commit()
        return True