from flask import Blueprint

bp = Blueprint('booknotes', __name__)

from diary.booknotes import routes