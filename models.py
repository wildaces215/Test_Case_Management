from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class TestCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))
    status = db.Column(db.String(20))
    execution_date = db.Column(db.Date)
    result = db.Column(db.String(20))
    priority = db.Column(db.String(20))
    requirements = db.relationship('Requirement', secondary='testcase_requirement', backref='test_cases')

class Requirement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))

# Association table for the many-to-many relationship
testcase_requirement = db.Table('testcase_requirement',
    db.Column('testcase_id', db.Integer, db.ForeignKey('test_case.id')),
    db.Column('requirement_id', db.Integer, db.ForeignKey('requirement.id'))
)
