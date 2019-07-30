# importing SQLAlchemy object from the main file(app.py)
from app import db

class DepartmentModel(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True,nullable=False)
