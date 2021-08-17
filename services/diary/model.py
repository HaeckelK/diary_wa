from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class DefaultCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
