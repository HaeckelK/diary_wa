from flask import Blueprint

bp = Blueprint('articles', __name__)

from diary.articles import routes