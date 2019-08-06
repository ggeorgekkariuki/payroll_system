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