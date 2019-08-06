from app import db

class PayrollModel(db.Model):
    __tablename__ = 'payrolls'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), nullable=False)
    month = db.Column(db.String(20), nullable=False)
    overtime = db.Column(db.Float, nullable=False)
    loan_deducted = db.Column(db.Float, nullable=False)
    advance_pay = db.Column(db.Float, nullable=False)
    gross_salary = db.Column(db.Float, nullable=False)
    NSSF = db.Column(db.Float, nullable=False)
    taxable_income = db.Column(db.Float, nullable=False)
    PAYE = db.Column(db.Float, nullable=False)
    personal_relief = db.Column(db.Float, nullable=False)
    nhif_chargeable_income = db.Column(db.Float, nullable=False)
    NHIF = db.Column(db.Float, nullable=False)
    net_salary = db.Column(db.Float, nullable=True)
    take_home_pay = db.Column(db.Float, nullable=True)
    # Defining the Foreign Key for the departments Table
    employee_id = db.Column(db.Integer, db.ForeignKey('EmployeeModel.id'), nullable=False)
    employee = db.relationship('EmployeeModel', backref=db.backref("payrolls", single_parent=True, lazy=True))

    def insert_to_db(self):
        db.session.add(self)
        db.session.commit()
