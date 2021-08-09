from dataclasses import asdict
from datetime import datetime
import os

from flask import Flask, request

from database import ArticleDatabase

app = Flask(__name__)


def get_db():
    return ArticleDatabase(os.environ["SQLITE_DB_PATH"])


@app.route("/")
def index():
    return "Articles API"


@app.route("/articles", methods=["GET"])
def get_articles():
    db = get_db()
    articles = db.get_all_article()
    return articles


@app.route("/articles/<int:id>", methods=["GET"])
def get_article(id: int):
    db = get_db()
    articles = db.get_all_article()
    return asdict(articles[id])


@app.route("/articles", methods=["POST"])
def post_article():
    url = request.form.get("url")

    db = get_db()
    id = db.insert_article(url=url, date_added=today())
    articles = db.get_all_article()
    return asdict(articles[id])


def today(date_format: str = "%Y%m%d") -> str:
    return datetime.today().strftime(date_format)
