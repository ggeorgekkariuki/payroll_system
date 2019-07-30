# from app import db
#
# class PayrollModel(db.Model):
#     __tablename__ = 'payrolls'
#     id = db.Column(db.Integer, primary_key=True)
#     full_name = db.Column(db.String(50), nullable=False)
#
#     NHIF = db.Column(db.Integer, nullable=False)
#     net_salary = db.Column(db.Float, nullable=True)
#     # Defining the Foreign Key for the departments Table
#     employee_id = db.Column(db.Integer, db.ForeignKey('EmployeeModel.id'), nullable=False)
#     employee = db.relationship('EmployeeModel', backref=db.backref("payrolls", single_parent=True, lazy=True))