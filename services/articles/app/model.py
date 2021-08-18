from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, unique=True, nullable=False)
    date_added = db.Column(db.Integer, unique=False, nullable=False)
