from dataclasses import asdict
from datetime import datetime
import os

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["ARTICLES_DATABASE_URI"]
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, unique=True, nullable=False)
    date_added = db.Column(db.Integer, unique=False, nullable=False)


def serialize_article(article: Article):
    return {"id": article.id, "url": article.url, "date_added": article.date_added}


@app.route("/")
def index():
    return "Articles API"


@app.route("/articles", methods=["GET"])
def get_articles():
    articles = Article.query.all()
    return {x.id: serialize_article(x) for x in articles}


@app.route("/articles/<int:id>", methods=["GET"])
def get_article(id: int):
    articles = Article.query.all()
    data = {x.id: serialize_article(x) for x in articles}
    return data[id]


@app.route("/articles", methods=["POST"])
def post_article():
    url = request.form.get("url")

    article = Article(url=url, date_added=int(today()))
    db.session.add(article)
    db.session.commit()
    id = article.id

    articles = Article.query.all()
    data = {x.id: serialize_article(x) for x in articles}
    return data[id]


def today(date_format: str = "%Y%m%d") -> str:
    return datetime.today().strftime(date_format)
