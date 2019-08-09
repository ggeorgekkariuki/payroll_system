from app import db

from models.Departments import DepartmentModel

class EmployeeModel(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50),nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    kra_pin = db.Column(db.String(20), unique=True, nullable=False)
    email =db.Column(db.String, unique=True)
    national_id = db.Column(db.Integer,unique=True, nullable=False)
    basic_salary = db.Column(db.Float, nullable=False)
    benefits = db.Column(db.Float, nullable=True)
    # Defining the Foreign Key for the departments Table
    department_id = db.Column(db.Integer, db.ForeignKey('departments'
                                                        '.id'), nullable=False)
    department = db.relationship('DepartmentModel', backref=db.backref("employees", single_parent=True, lazy=True, cascade='all,delete')) # pseudocolumn for departments

    def insert_to_db(self): #create
        db.session.add(self)
        db.session.commit()

    @classmethod
    def fetch_by_mail(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def fetch_employee_by_id(cls, emp_id):
        return cls.query.filter_by(id=emp_id).first()

    @classmethod
    def fetch_all(cls):
        return cls.query.all()

    @classmethod
    def fetch_by_department(cls, dept_id):
        return cls.query.filter_by(department_id=dept_id)

    @classmethod #TODO: read on keyword functions & default functions
    def update_employee(cls, id, full_name=None, gender=None, kra_pin=None, email=None, national_id=None, basic_salary=None, benefits=None, department_id=None): #update
        record = cls.fetch_employee_by_id(id)
        if full_name:
            record.full_name = full_name
        if gender:
            record.gender = gender
        if kra_pin:
            record.kra_pin =kra_pin
        if email:
            record.email =email
        if national_id:
            record.national_id = national_id
        if basic_salary:
            record.basic_salary = basic_salary
        if benefits:
            record.benefits = benefits
        if department_id:
            record.department_id = department_id

        db.session.commit()
        return True

    @classmethod
    def delete_by_id(cls, id):
        record = cls.query.filter_by(id=id)
        record.delete()
        db.session.commit()
        return True