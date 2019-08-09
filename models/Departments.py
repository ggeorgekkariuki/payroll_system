# importing SQLAlchemy object from the main file(app.py)
from app import db

class DepartmentModel(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True,nullable=False)

    def insert_to_db(self): #create
        db.session.add(self)
        db.session.commit()

    @classmethod
    def fetch_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def fetch_by_department(cls, dept_id):
        return cls.query.filter_by(id=dept_id).first()

    @classmethod
    def fetch_all(cls):
        return cls.query.all()


    @classmethod
    def fetch_total_payroll_department_id(cls,id):
        this_dept = cls.fetch_by_department(id)
        total_payroll = 0
        for each_employee in this_dept.employees:
            total_payroll += each_employee.basic_salary + each_employee.benefits

        return total_payroll

    @classmethod
    def update_department(cls, id, name=None):
        record = cls.fetch_by_department(id)
        if name:
            record.name = name
        db.session.commit()
        return True

    @classmethod
    def delete_by_id(cls, id):
        record = cls.query.filter_by(id=id)
        record.delete()
        db.session.commit()
        return True