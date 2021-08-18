from datetime import datetime
import os

from flask import Flask, request


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["ARTICLES_DATABASE_URI"]

    from app.model import db, Article

    db.init_app(app)

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
        try:
            return data[id]
        except KeyError:
            return f"Record not found for id {id}", 400

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

    return app


def today(date_format: str = "%Y%m%d") -> str:
    return datetime.today().strftime(date_format)
