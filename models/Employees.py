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
    department = db.relationship('DepartmentModel', backref=db.backref("employees", single_parent=True, lazy=True)) # pseudocolumn for departments

    def insert_to_db(self): #create
        db.session.add(self)
        db.session.commit()

    @classmethod
    def fetch_by_mail(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def fetch_all(cls):
        return cls.query.all()

    @classmethod
    def fetch_by_department(cls, dept_id):
        return cls.query.filter_by(department_id=dept_id)